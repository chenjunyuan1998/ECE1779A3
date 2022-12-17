from flask import Flask

webapp = Flask(__name__)

if __name__ == '__main__':
    webapp.run('0.0.0.0',5000,debug=True,threaded=True)