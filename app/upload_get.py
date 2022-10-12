from flask import render_template, url_for, request, flash, redirect

import BackendApp.db
from app import webapp, memcache
from flask import json
import os


@webapp.route('/upload_search')
def upload_search():
    return render_template("upload_search.html")

@webapp.route('/search', methods=['POST'])
def search():

    key = request.form.get('key')
    result = memcache.get(key)

    response = webapp.response_class(
        response=json.dumps("Unknown key"),
        status=400,
        mimetype='application/json'
    )

    if result == -1:  # if can't get location from memcache, get location from DB
        DBresult = BackendApp.db.get_image_with_key(key) # method from db to get image location using specific key
        if DBresult is None:
            return response
        else:
            fname = os.path.join('app/static/images', key)
            memcache.put(key,fname)
            return render_template("display_image.html", result = fname[4:])

        return response
    else:
        return render_template("display_image.html", result=result[4:])


@webapp.route('/upload', methods=['POST'])
def upload():

    key = request.form.get('key')

    new_image = request.files['file']
    fname = os.path.join('app/static/images', key)
    new_image.save(fname)
    print(fname)

    #value = request.form.get('file')
    memcache.put(key, fname)
    BackendApp.db.put_image(key,fname,'app/static/images') # method from db to put image



    response = webapp.response_class(
        response=json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )
    return response


