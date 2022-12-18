from flask import Flask, render_template

webapp = Flask(__name__)

if __name__ == '__main__':
    webapp.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
