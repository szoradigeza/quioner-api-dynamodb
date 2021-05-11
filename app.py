from flask import Flask
from flask import request
from flask import jsonify
import boto3

ddb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')


app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello_():
    print(list(ddb.tables.all()))
    return jsonify({"response" : "Succesfull!"}), 200

