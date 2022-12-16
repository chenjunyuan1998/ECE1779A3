import requests
from flask import render_template, url_for, request, flash, redirect, make_response
from app import webapp
from flask import json
import os
cache_http = 'http://localhost:5002'
account_http= 'http://localhost:5001'

@webapp.route('/profile', methods=['GET'])
#@login_required
def profile():

    return render_template('profile.html')


@webapp.route('/upload', methods=['GET', 'POST'])
#@login_required
def upload():#done
    if request.method == 'POST':
        key = request.form.get('key')
        new_image = request.files['file']
        username = request.cookies.get('username')
        req = {
            'key': key,
            'username': username,
            'value': new_image,
        }
        resp = requests.post(cache_http + '/put', json=req)
        if resp.json() == 'OK':
            resp_space = requests.post(cache_http + '/showSpaceUsed', json=req)
            return render_template('profile.html', status='Uploaded',user=username,space= resp_space)
        else:
            resp_space = requests.post(cache_http + '/showSpaceUsed', json=req)
            return render_template('profile.html', status='Fail to Upload',user=username,space= resp_space)


@webapp.route('/config', methods=['GET', 'POST'])
#@login_required
def config():#done
    if request.method == 'POST':
        capacity = request.form.get('capacity')
        username = request.cookies.get('username')
        req = {
            'capacity': capacity,
            'username': username,
        }
        cache_resp = requests.post(cache_http + '/setCap', json=req)
        #account_resp = requests.post(account_http + '/updateCapacity', json=req)
        if cache_resp.json() == 'OK' :
            resp_space = requests.post(cache_http + '/showSpaceUsed', json=req)
            return render_template('profile.html', status='Capacity Set',user=username,space= resp_space)
        else:
            resp_space = requests.post(cache_http + '/showSpaceUsed', json=req)
            return render_template('profile.html', status='Fail to Set',user=username,space= resp_space)

@webapp.route('/view_all_image', methods=['GET', 'POST'])
#@login_required
def view_all_image():#done
     username = request.cookies.get('username')
     req = {
         'username': username,
     }
     resp = requests.post(cache_http + '/showGallery', json=req)
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
     key = request.form.get('key')
     req = {
         'username': username,
         'key': key,
     }
     resp = requests.post(cache_http + '/deleteValue', json=req)
     if resp.json() == 'OK':
        return redirect('/view_all_image')
     else:
        return render_template('view.html', status='Fail to delete')