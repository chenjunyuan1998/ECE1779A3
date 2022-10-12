from flask import render_template, url_for, request

import BackendApp.db
from app import webapp, memcache
from flask import json


@webapp.route('/display_key')
def display_key():
    keyList = BackendApp.db.get_key_list()
    return render_template("display_key.html", keyList = keyList)