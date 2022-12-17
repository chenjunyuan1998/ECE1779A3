
from boto3.dynamodb.conditions import Key
from flask import Flask, render_template
from app.auth import auth_routes
from app.profile import profile_routes
#global memcache

webapp = Flask(__name__)
webapp.register_blueprint(auth_routes)
webapp.register_blueprint(profile_routes)
from app import auth
from app import profile

@webapp.route('/')
def main(): #very first page
    return render_template('login.html')