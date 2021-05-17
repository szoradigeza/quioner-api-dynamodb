from helpers.request_check import *
from helpers.json_resp import json_response
from helpers.dynamodb import ddb
from datetime import datetime
from flask_jwt_extended import create_access_token
from flask import jsonify
import uuid
from helpers.hash import verify_hash, generate_hash



def handle_get_users(request):
    table = ddb.Table('user')
    if request.method == 'GET':
        users = table.scan(ProjectionExpression= 'username, rights')['Items']
        return json_response(users)

def user_registration(request):
    table = ddb.Table('user')
    if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            name = request.form['name']
            right = request.form['right']
    key = {'username': username}
    user = table.get_item(Key=key)
    if user.get('Item'):
        return json_response({"message": "User {} already exists".format(username)})
    table.put_item(Item={
        'id': str(uuid.uuid1()),
        'username': username,
        'name': name,
        'password_hash': generate_hash(password),
        'rights': right,
        'created': datetime.today().strftime('%Y-%m-%d')
    })
    return json_response({"message": "User {} was created!".format(username)})

def handle_login(request):
    username = request.form['username']
    password = request.form['password']
    table = ddb.Table('user')
    key = {'username': username}
    user = table.get_item(Key=key)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401
    role = user.get('Item')['rights']
    token = { 
        'username': username,
        'role': role
    }
    access_token = create_access_token(identity=token)
    return jsonify(access_token=access_token)

def handle_set_password(request):
    table = ddb.Table('user')
    username = request.form['username']
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    key = {'username': username}
    user = table.get_item(Key=key)
    if verify_hash(old_password, user.get('Item')['password_hash']):
        response = table.update_item(
        Key=key,
        UpdateExpression="set password_hash=:passw",
        ExpressionAttributeValues={
            ':passw': generate_hash(new_password)
        },
        ReturnValues="UPDATED_NEW"
    )
        return jsonify({"message": "Complete!"}), 200
    else:
        return jsonify({"message": "Wrong password!!"}), 200


def handle_get_rights(request):
    table = ddb.Table('user')
    users_right = table.scan(ProjectionExpression= 'rights')['Items']
    possible_rights = []
    for user in users_right:
        if user['rights'] not in possible_rights:
            possible_rights.append(user['rights'])
    return jsonify(rights=possible_rights)


def handle_admin_change_password(request):
    try:
        table = ddb.Table('user')
        username = request.form['username']
        new_password = request.form['new_password']
        right = request.form['right']
        key = {'username': username}
        if new_password:
            response = table.update_item(
            Key=key,
            UpdateExpression="set password_hash=:passw, rights=:right ",
            ExpressionAttributeValues={
                ':passw': generate_hash(new_password),
                ':right': right
            },
            ReturnValues="UPDATED_NEW"
        )
        return jsonify({"message": "User password and right changed!"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 200

def handle_delete_user(request):
    try:
        username = request.form['username']
        table = ddb.Table('user')
        key = {'username': username}
        table.delete_item(
        Key=key
        )
        return jsonify({"message": "User has been deleted!"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 200

def handle_get_name_by_username(request):
        username = request.form['username']
        table = ddb.Table('user')
        key = {'username': username}
        user = table.get_item(Key=key)
        name = user.get('Item')['name']
        return jsonify(name=name)