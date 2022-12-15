from apscheduler.schedulers.background import BackgroundScheduler
from boto3.dynamodb.conditions import Key
from flask import Flask
from flask_login import LoginManager, UserMixin

#global memcache
from Backend.DynamoDB.db_account_restful import credential_table

webapp = Flask(__name__)
webapp.secret_key = 'secret key abc'


def create_app():
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(webapp)

    @login_manager.user_loader
    #load user from session, can not used for the first time login
    def loader(user_id):
        response = credential_table.query(
            KeyConditionExpression=Key('username').eq(user_id))

        if response["Count"] == 0:
            return
        user = User(username=response['Items'][0]["username"], password=response['Items'][0]["password"],
                    image=response['Items'][0]["image"])
        return user


class User(UserMixin):
    def __init__(self, username, password, image):
        self.username = username
        self.password = password
        self.image = image



def get_user(username,password):
    """

    :param username:
    :param password:
    :return: user object that include username, password, image list

    to be complete
    """
    #get user from db
    #user = User.query.filter_by().first()
    return user