
from boto3.dynamodb.conditions import Key
from flask import Flask
#global memcache

webapp = Flask(__name__)

if __name__ == '__main__':
    webapp.run('0.0.0.0',5000,debug=True,threaded=True)