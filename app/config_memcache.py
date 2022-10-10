from flask import render_template, url_for, request
from app import webapp, memcache
from flask import json


@webapp.route('/config_memcache')
def config_memcache():
    return render_template("config_memcache.html")