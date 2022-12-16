import json
import boto3
from flask import request
from Backend.DynamoDB import webapp
from Backend.Config import aws_config

dynamodb = boto3.resource('dynamodb', aws_access_key_id=aws_config['aws_access_key_id'],
                          aws_secret_access_key=aws_config['aws_secret_access_key'])
credential_table = dynamodb.Table('UserCredentialTable')


@webapp.route('/signIn', methods=['POST'])
def sign_in():
    req_json = request.get_json(force=True)
    username = req_json['username']
    password = req_json['password']

    response = credential_table.get_item(Key={'username': username})
    print(response)
    if response['Item']:
        recorded_password = response['Item']['password']
        if password == recorded_password:
            return {
                'statusCode': 200,
                'body': json.dumps("CORRECT_PWD")
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps("INCORRECT_PWD")
            }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps("INVALID_USER")
        }


@webapp.route('/signUp', methods=['POST'])
def sign_up():
    req_json = request.get_json(force=True)
    username = req_json["username"]
    password = req_json["password"]

    response = credential_table.get_item(Key={'username': username})
    print(response)
    if response['Item']:
        return {
            'statusCode': 200,
            'body': json.dumps("ALREADY_EXISTS")
        }
    else:
        if username.isalnum():  # username can only contain alphabet letters and numbers
            credential_response = credential_table.put_item(
                Item={
                    'username': username,
                    'password': password,
                    # 'capacity': 10
                }
            )
            return {
                'statusCode': 200,
                'body': json.dumps("CREATED_USER")
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps("INVALID_NAME")
            }


@webapp.route('/closeAccount', methods=['POST'])
def close_account():
    req_json = request.get_json(force=True)
    username = req_json["username"]
    password = req_json["password"]

    response = credential_table.get_item(Key={'username': username})
    print(response)
    if response['Item']:
        recorded_password = response['Item']['password']
        if password == recorded_password:
            credential_response = credential_table.delete_item(
                Item={
                    'username': username
                }
            )
            return {
                'statusCode': 200,
                'body': json.dumps("DELETED_USER")
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps("DELETE_FAILED")
            }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps("USER_NOT_FOUND")
        }


# @webapp.route('/updateCapacity', methods=['POST'])
# def update_capacity():
#     req_json = request.get_json(force=True)
#     username = req_json['username']
#     capacity = req_json['capacity']
#
#     response = credential_table.get_item(Key={'username': username})
#     if response['Item']:
#         response = credential_table.update_item(
#             Key={'username': username},
#             UpdateExpression="SET capacity = :c",
#             ExpressionAttributeValues={
#                 ':c': capacity,
#             },
#             ReturnValues="UPDATED_NEW"
#         )
#         return {
#             'statusCode': 200,
#             'body': json.dumps("UPDATED_CAPACITY")
#         }
#     else:
#         return {
#             'statusCode': 200,
#             'body': json.dumps("USER_NOT_FOUND")
#         }
