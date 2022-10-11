from flask import render_template, url_for, request
from app import webapp, memcache
from flask import json


@webapp.route('/image', methods=["GET"])
def display_image():
    return render_template("display_image.html")

