from flask import Flask, render_template
from test_zappa.app import webapp

@webapp.route('/')
def login():
    return render_template("login.html")

@webapp.route('/api')
def api():
    return {'hello': 'world'}
