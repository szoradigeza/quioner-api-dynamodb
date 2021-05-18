from flask import Flask
from flask import request
from flask import jsonify
import boto3
from helpers.dynamodb import *
from flask import request
from helpers.json_resp import json_response
from resources.users import *
from resources.questions import *
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask import jsonify


ddb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config['JWT_TOKEN_LOCATION'] = ['headers']
jwt = JWTManager(app)

#init_table()

@app.route("/login", methods=["POST"])
def post_login():
    return handle_login(request)

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route('/')
def index():
    return json_response({"message": "Hello, world!"})


@app.route('/users/getusers', methods=['GET'])
def get_users():
    return handle_get_users(request)

@app.route('/users/registration', methods=['POST'])
def post_user_registration():
    return user_registration(request)

@app.route('/users/setnewpassword', methods=['POST'])
def post_set_new_password():
    return handle_set_password(request)

@app.route('/users/getrights', methods=['GET'])
def get_rights():
    return handle_get_rights(request)

@app.route('/users/changepassword', methods=['POST'])
def post_admin_change_password():
    return handle_admin_change_password(request)

@app.route('/users/deleteuser', methods=['POST'])
def post_delete_user():
    return handle_delete_user(request)


@app.route('/users/getnamebyusername', methods=['POST'])
def post_get_name_by_username():
    return handle_get_name_by_username(request)


#QUESTIONS
@app.route('/question/addquestion', methods=['POST'])
def post_add_question():
    return handle_add_question(request)

@app.route('/question/editquestion', methods=['POST'])
def post_edit_question():
    return handle_edit_question(request)

@app.route('/question/delete-question', methods=['POST'])
def post_delete_question():
    return handle_delete_question(request)

@app.route('/question/getquestions', methods=['GET'])
def get_list_questions():
    return handle_get_all_questions()



@app.route('/question/newcategory', methods=['POST'])
def post_new_category():
    return handle_create_new_question_category(request)

@app.route('/question/image-upload', methods=['POST'])
def post_upload_question_image():
    return handle_add_question_image(request)

@app.route('/question/image/<filename>', methods=['GET'])
def get_question_image():
    return handle_get_question_image(request)


@app.route('/question/reviewed', methods=['GET'])
def get_reviewed_questions():
    return handle_get_reviewed_questions()
