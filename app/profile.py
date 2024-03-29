import requests
from flask import render_template, url_for, request, flash, redirect, make_response, session

from Backend.Storage import store_global
from app.main import webapp
import base64
from flask import json
import os

cache_http = 'http://localhost:5002'
account_http = 'http://localhost:5001'

# cache_http = 'https://4a8pwpqo5g.execute-api.us-east-1.amazonaws.com/storage'
# account_http = 'https://xwtbovbyfj.execute-api.us-east-1.amazonaws.com/db'


@webapp.route('/profile', methods=['GET', 'POST'])
#@login_required
def profile():
    username = request.cookies.get('username')
    req = {'username' : username}
    resp_space = requests.get(cache_http + '/showSpaceUsed', json=req)
    return render_template('profile.html', status='Capacity Set', user=username, space=resp_space.json())


@webapp.route('/upload', methods=['GET', 'POST'])
#@login_required
def upload():#done
    if request.method == 'POST':
        key = request.form.get('key')
        new_image = request.files['file']
        username = request.cookies.get('username')
        base64_image = base64.b64encode(new_image.read())
        print('username：', username)
        req = {
            'key': key,
            'username': username,
            'value': base64_image,
        }
        resp = requests.post(cache_http + '/put', json=req)
        print('storage_resp:', resp)
        if resp.json() == 1:
            resp_space = requests.get(cache_http + '/showSpaceUsed', json=req)
            return render_template('profile.html', status='Uploaded', user=username, space=resp_space.json())
        elif resp.json() == 0:
            resp_space = requests.get(cache_http + '/showSpaceUsed', json=req)
            return render_template('profile.html', status='Fail to Upload', user=username, space=resp_space.json())
        else:
            resp_space = requests.get(cache_http + '/showSpaceUsed', json=req)
            return render_template('profile.html', status='Error occurred', user=username, space=resp_space.json())


@webapp.route('/config', methods=['GET', 'POST'])
#@login_required
def config():#done
    if request.method == 'POST':
        capacity = request.form.get('capacity')
        username = request.cookies.get('username')
        print('username：', username)
        req = {
            'capacity': capacity,
            'username': username,
        }
        cache_resp = requests.post(cache_http + '/setCap', json=req)
        if cache_resp.json() == 'OK':
            resp_space = requests.get(cache_http + '/showSpaceUsed', json=req)
            return render_template('profile.html', status='Capacity Set', user=username, space=resp_space.json())
        else:
            resp_space = requests.get(cache_http + '/showSpaceUsed', json=req)
            return render_template('profile.html', status='Fail to Set', user=username, space=resp_space.json())


@webapp.route('/view_all_keys', methods=['GET', 'POST'])
#@login_required
def view_all_image():#done
    username = request.cookies.get('username')
    print('username：', username)
    req = {
        'username': username,
    }
    resp = requests.get(cache_http + '/showKeys', json=req).json()
    print('image_resp:', resp)
    print(type(resp))
    resp1 = make_response(render_template('view.html', items=resp))
    resp1.set_cookie('username', username)
    return resp1



@webapp.route('/view_image', methods=['GET', 'POST'])
#@login_required
def view_image():#done
    username = request.cookies.get('username')
    key = request.form.get('key')
    print('username：', username)
    req = {
        'username': username,
        'key': key,
    }
    resp = requests.post(cache_http + '/get', json=req)
    print('image_resp:', resp)
    print(type(resp))
    resp1 = make_response(render_template('view_image.html', image=resp.json()))
    resp1.set_cookie('username', username)
    return resp1



@webapp.route('/delete_image', methods=['GET', 'POST'])
#@login_required
def delete_image():#done
    username = request.cookies.get('username')
    print('username：', username)
    key = request.form.get('key')
    req = {
     'username': username,
     'key': key,
    }
    resp = requests.post(cache_http + '/deleteValue', json=req)
    print('cache_resp:', resp)
    resp_key = requests.get(cache_http + '/showKeys', json=req).json()
    print('image_resp:', resp_key)
    return render_template('view.html', items=resp_key)

@webapp.route('/update', methods=['GET', 'POST'])
#@login_required
def update():#done
    if request.method == 'POST':
        key = request.form.get('key')
        new_image = request.files['file']
        username = request.cookies.get('username')
        print('username：', username)
        base64_image = base64.b64encode(new_image.read())
        req = {
            'key': key,
            'username': username,
            'value': base64_image,
        }
        resp = requests.post(cache_http + '/put', json=req)
        print('storage_resp:', resp)
        resp_key = requests.get(cache_http + '/showKeys', json=req).json()
        print('storage_resp:', resp_key)
        if resp.json() == 1:
            return render_template('view.html', status='Updated',items=resp_key)
        elif resp.json() == 0:
            return render_template('view.html', status='Fail to update',items=resp_key)
        else:
            return render_template('view.html', status='Error occurred',items=resp_key)
