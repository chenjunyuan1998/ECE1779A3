
from boto3.dynamodb.conditions import Key
from flask import Flask

webapp = Flask(__name__)

if __name__ == '__main__':
    webapp.run('0.0.0.0', debug=True, threaded=True)
