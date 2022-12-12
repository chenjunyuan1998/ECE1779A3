import json
import boto3

dynamodb = boto3.resource('dynamodb')
credential_table = dynamodb.Table('UserCredentialTable')
image_table = dynamodb.Table('UserImageTable')


def sign_in(event, context):
    username = event['username']
    password = event['password']

    response = credential_table.get_item(Key={'username': username})
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


def sign_up(event, context):
    username = event["username"]
    password = event["password"]

    response = credential_table.get_item(Key={'username': username})
    if response['Item']:
        return {
            'statusCode': 200,
            'body': json.dumps("ALREADY_EXISTS")
        }
    else:
        credential_response = credential_table.put_item(
            Item={
                'username': username,
                'password': password,
                'capacity': 10
            }
        )

        image_response = image_table.put_item(
            Item={
                'user': username
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps("CREATED_USER")
        }


def close_account(event, context):
    username = event["username"]
    password = event["password"]

    response = credential_table.get_item(Key={'username': username})
    if response['Item']:
        recorded_password = response['Item']['password']
        if password == recorded_password:
            credential_response = credential_table.delete_item(
                Item={
                    'username': username
                }
            )
            image_response = image_table.delete_item(
                Item={
                    'user': username
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


def update_capacity(event, context):
    username = event['username']
    capacity = event['capacity']

    response = credential_table.get_item(Key={'username': username})
    if response['Item']:
        response = credential_table.update_item(
            Key={'username': username},
            UpdateExpression="SET capacity = :c",
            ExpressionAttributeValues={
                ':c': capacity,
            },
            ReturnValues="UPDATED_NEW"
        )
        return {
            'statusCode': 200,
            'body': json.dumps("UPDATED_CAPACITY")
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps("USER_NOT_FOUND")
        }
