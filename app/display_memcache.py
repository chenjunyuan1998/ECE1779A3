from flask import render_template, url_for, request
from app import webapp, memcache
from flask import json


@webapp.route('/display_memcache')
def display_memcache():
    return render_template("display_memcache.html")