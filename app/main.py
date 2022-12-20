from flask import Flask
from auth import auth_routes
from profile import profile_routes

webapp = Flask(__name__)
webapp.register_blueprint(auth_routes)
webapp.register_blueprint(profile_routes)

if __name__ == '__main__':
    webapp.run('0.0.0.0', debug=True, threaded=True)
