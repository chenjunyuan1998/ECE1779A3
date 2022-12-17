import os, sys, base64
import boto3
from Backend.Config import aws_config, bucket

s3 = boto3.client('s3', region_name='us-east-1', aws_access_key_id=aws_config['aws_access_key_id'],
                  aws_secret_access_key=aws_config['aws_secret_access_key'])


def get_size(value):
    #_, extension = os.path.splitext(value.filename)
    #base64_image = base64.b64encode(value.read())
    image_size = sys.getsizeof(value)
    return image_size


def put_image_to_s3(user, key, value):
    """
    Put image to s3 bucket.
    """
    #_, extension = os.path.splitext(value.filename)
    #base64_image = base64.b64encode(value.read())
    image_key = str(user) + "::" + str(key)
    s3.put_object(Body=value, Key=image_key, Bucket=bucket, ContentType='image')
    image_url = 'https://s3.amazonaws.com/' + bucket + '/' + image_key + '.jpg'
    #image_size = sys.getsizeof(base64_image)
    image_size = sys.getsizeof(value)
    return image_size


def get_image_from_s3(user, key):
    """
    Get image from s3 bucket.
    """
    image_key = str(user) + "::" + str(key)
    with open('Temp.txt', 'wb') as file:
        s3.download_fileobj(bucket, image_key, file)
    with open('Temp.txt', 'rb') as file:
        base64_image = file.read().decode('utf-8')
    file.close()
    os.remove("Temp.txt")
    # print("Got image from s3 bucket: ", image_key)
    return base64_image


def delete_image_from_s3(user, key):
    """
    Delete image from s3 bucket.
    """
    image = get_image_from_s3(user, key)
    image_size = sys.getsizeof(image)

    image_key = str(user) + "::" + str(key)
    s3.delete_object(Key=image_key)
    # print("Deleted image from s3 bucket: ", image_key)

    return image_size
