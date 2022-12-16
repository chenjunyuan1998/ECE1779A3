from flask import Flask

webapp = Flask(__name__)

from Backend.DynamoDB.db_account_restful import *