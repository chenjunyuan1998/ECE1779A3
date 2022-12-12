import json
import boto3

dynamodb = boto3.resource('dynamodb')
image_table = dynamodb.Table('UserImageTable')


def get_image(event, context):
    user = event['user']
    key = event['key']

    response = image_table.get_item(Key={'user': user})
    if response['Item']:
        if response['Item'][key]:
            count = response['Item'][key]
            response = image_table.update_item(
                Key={'user': user},
                UpdateExpression="SET " + str(key) + " = :c",
                ExpressionAttributeValues={
                    ':c': count + 1,
                },
                ReturnValues="UPDATED_NEW"
            )
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item'][key])
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps("KEY_NOT_FOUND")
            }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps("USER_NOT_FOUND")
        }


def put_image(event, context):
    user = event['user']
    key = event['key']

    response = image_table.get_item(Key={'user': user})
    if response['Item']:
        if response['Item'][key]:  # if key exists, update <key, count> pair, count += 1
            count = response['Item'][key]
            response = image_table.update_item(
                Key={'user': user},
                UpdateExpression="SET " + str(key) + " = :c",
                ExpressionAttributeValues={
                    ':c': count + 1,
                },
                ReturnValues="UPDATED_NEW"
            )
        else:  # if key doesn't exist, create new <key, count> pair with count = 0
            response = image_table.update_item(
                Key={'user': user},
                UpdateExpression="SET " + str(key) + " = :c",
                ExpressionAttributeValues={
                    ':c': 0,
                },
                ReturnValues="UPDATED_NEW"
            )
        return {
            'statusCode': 200,
            'body': json.dumps("UPLOADED")
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps("USER_NOT_FOUND")
        }


def delete_image(event, context):
    user = event['user']
    key = event['key']

    response = image_table.get_item(Key={'user': user})
    if response['Item']:
        if response['Item'][key]:
            response = image_table.update_item(
                    Key={'user': user},
                    UpdateExpression="REMOVE " + str(key) + " = :c",
                    ExpressionAttributeValues={
                        ':c': response['Item'][key],
                    },
                    ReturnValues="UPDATED_NEW"
                )
            return {
                'statusCode': 200,
                'body': json.dumps("DELETED")
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps("KEY_NOT_FOUND")
            }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps("USER_NOT_FOUND")
        }


def get_count(event, context):
    user = event['user']
    key = event['key']

    response = image_table.get_item(Key={'user': user})
    if response['Item']:
        if response['Item'][key]:
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item'][key])
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps("KEY_NOT_FOUND")
            }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps("USER_NOT_FOUND")
        }

