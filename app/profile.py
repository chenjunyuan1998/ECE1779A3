import requests
from flask import render_template, url_for, request, flash, redirect, make_response
from app import webapp
import base64
from flask import json
import os
cache_http = 'http://localhost:5002'
account_http = 'http://localhost:5001'


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


@webapp.route('/view_all_image', methods=['GET', 'POST'])
#@login_required
def view_all_image():#done
    username = request.cookies.get('username')
    print('username：', username)
    req = {
        'username': username,
    }
    resp = requests.get(cache_http + '/showGallery', json=req).json()
    print('image_resp:', resp)
    if resp:
        resp1 = make_response(render_template('view.html', items=resp))
        resp1.set_cookie('username', username)
        return resp1
    else:
        return 'There is no image.'


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
    if resp.json() == 'OK':
        return redirect('/view_all_image')
    else:
        return render_template('view.html', status='Fail to delete')
