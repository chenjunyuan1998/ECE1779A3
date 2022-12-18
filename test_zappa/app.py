from flask import Flask, render_template

webapp = Flask(__name__)
@webapp.route("/")
def hello_world():
    return "hello"

@webapp.route('/api')
def api():
    return {'hello': 'world'}

if __name__ == '__main__':
    webapp.run()
