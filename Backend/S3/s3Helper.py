import os, sys, base64
import boto3
from Backend.Config import aws_config, bucket

s3 = boto3.client('s3', region_name='us-east-1', aws_access_key_id=aws_config['aws_access_key_id'],
                  aws_secret_access_key=aws_config['aws_secret_access_key'])


def put_image_to_s3(request, key):
    """
    Put image to s3 bucket.
    """
    file = request.files['file']
    _, extension = os.path.splitext(file.filename)
    try:
        base64_image = base64.b64encode(file.read())
        s3.put_object(Body=base64_image, Key=key, Bucket=bucket, ContentType='image')
        print("Saved image to s3 bucket.")
        image_url = 'https://s3.amazonaws.com/' + bucket + '/' + key + extension
        image_size = sys.getsizeof(base64_image)
        response = {
            'image_key': key,
            'image_url': key,
            'image_size': key
        }
        return response
    except:
        return "UPLOAD_FAILED"


def get_image_from_s3(key):
    """
    Get image from s3 bucket.
    """
    with open('Temp.txt', 'wb') as file:
        s3.download_fileobj(bucket, key, file)
    with open('Temp.txt', 'rb') as file:
        base64_image = file.read().decode('utf-8')
    file.close()
    os.remove("Temp.txt")
    print("Got image from s3 bucket: ", key)
    return base64_image
