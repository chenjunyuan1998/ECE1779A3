from apscheduler.schedulers.background import BackgroundScheduler
from flask import render_template, url_for, request
from app import webapp, memcache
from flask import json


@webapp.route('/')
def main():
    return render_template("main.html")