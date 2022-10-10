from flask import render_template, url_for, request
from app import webapp, memcache
from flask import json


@webapp.route('/display_key')
def display_key():
    keyList = memcache.keyAvaliable()
    return render_template("display_key.html", keyList = keyList)