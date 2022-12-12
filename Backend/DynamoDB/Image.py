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
    image = event['image']

    response = image_table.get_item(Key={'user': user})
    if response['Item']:
        response = image_table.update_item(
            Key={'user': user},
            UpdateExpression="SET " + key + " = :i",
            ExpressionAttributeValues={
                ':i': image,
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
    image = event['image']

    response = image_table.get_item(Key={'user': user})
    if response['Item']:
        if response['Item'][key]:
            response = image_table.update_item(
                    Key={'user': user},
                    UpdateExpression="REMOVE " + key + " = :i",
                    ExpressionAttributeValues={
                        ':i': image,
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
