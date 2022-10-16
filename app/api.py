from email.mime import multipart

import requests
from data.decorators import data
from form import form

from BackendApp import db
import BackendApp
from flask import request
import BackendApp.db
from app import webapp, memcache
import os


@webapp.route('/api/list_keys', methods=['GET', 'POST'])
def test_display_key():
    keyList = BackendApp.db.get_key_list()
    display_list = []
    for key in keyList:
        display_list.append(key[0])

    return {
        "success": "true",
        "keys": display_list
    }


@webapp.route('/api/key/<key_value>', methods=['GET','POST'])
def test_search(key_value):
    key = key_value
    result = memcache.get(key)

    if result == -1:
        DBresult = BackendApp.db.get_image_with_key(key)  # method from db to get image location using specific key
        if DBresult is None:
            return {
                "success": "false",
                "error": {
                    "code": 404,
                    "message": "Invalid key"
                }
            }
        else:
            fname = os.path.join('app/static/images', key)
            memcache.put(key, fname)
            return {
                "success": "true",
                "content": fname
            }


@webapp.route('/api/upload', methods=['POST'])
def test_upload():
    key = request.form.get("key")

    if key == '' or key is None:
        return {
            "success": "false",
            "error": {
                "code": 404,
                "message": "Missing key"
            }
        }

    if request.files.get('file') is None or request.files['file'].getbuffer().nbytes == 0:
        return {
            "success": "false",
            "error": {
                "code": 404,
                "message": "Missing file"
            }
        }



    new_image = request.files['file']
    fname = os.path.join('app/static/images', key)
    new_image.save(fname)
    print(fname)

    memcache.put(key, fname)
    BackendApp.db.put_image(key, fname, 'app/static/images')

    return {
        "success": "true"
    }
