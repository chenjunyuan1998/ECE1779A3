import json, requests
import boto3
from flask import Blueprint, request
from Config import aws_config

dynamodb = boto3.resource('dynamodb', aws_access_key_id=aws_config['aws_access_key_id'],
                          aws_secret_access_key=aws_config['aws_secret_access_key'])
credential_table = dynamodb.Table('UserCredentialTable')

storage_http = 'http://54.197.199.59:5002'

db_routes = Blueprint('db_routes', __name__)


@db_routes.route('/signIn', methods=['POST'])
def sign_in():
    req_json = request.get_json(force=True)
    username = req_json['username']
    password = req_json['password']

    response = credential_table.get_item(Key={'username': username})
    print(response)
    if 'Item' in response:
        recorded_password = response['Item']['password']
        print("password: ", password, ", recorded_password: ", recorded_password)
        if password == recorded_password:
            return json.dumps("CORRECT_PWD")
        else:
            return json.dumps("INCORRECT_PWD")
    else:
        return json.dumps("INVALID_USER")


@db_routes.route('/signUp', methods=['POST'])
def sign_up():
    req_json = request.get_json(force=True)
    username = req_json["username"]
    password = req_json["password"]

    response = credential_table.get_item(Key={'username': username})
    print(response)
    if 'Item' in response:
        return json.dumps("ALREADY_EXISTS")
    else:
        print("username.isalnum(): ", username.isalnum())
        if username.isalnum():  # username can only contain alphabet letters and numbers
            req = {
                'username': username
            }
            adduser_response = requests.post(storage_http + '/addUser', json=req)
            print("if add user success ", adduser_response.json())
            credential_response = credential_table.put_item(
                Item={
                    'username': username,
                    'password': password
                }
            )
            return json.dumps("CREATED_USER")
        else:
            return json.dumps("INVALID_NAME")


@db_routes.route('/closeAccount', methods=['POST'])
def close_account():
    req_json = request.get_json(force=True)
    username = req_json["username"]
    password = req_json["password"]

    response = credential_table.get_item(Key={'username': username})
    print(response)
    if 'Item' in response:
        recorded_password = response['Item']['password']
        if password == recorded_password:
            credential_response = credential_table.delete_item(Key={'username': username})
            return json.dumps("DELETED_USER")
        else:
            return json.dumps("DELETE_FAILED")
    else:
        return json.dumps("USER_NOT_FOUND")

