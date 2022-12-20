from flask import Flask
from db_account_restful import db_routes

webapp = Flask(__name__)
webapp.register_blueprint(db_routes)

if __name__ == '__main__':
    webapp.run('0.0.0.0', debug=True, threaded=True)
