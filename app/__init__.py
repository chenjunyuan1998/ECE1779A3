
from boto3.dynamodb.conditions import Key
from flask import Flask
#global memcache

webapp = Flask(__name__)

from app import auth
from app import profile

