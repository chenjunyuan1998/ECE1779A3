import requests
from flask import render_template, url_for, request, flash, redirect
from flask_login import login_required, current_user

from app import webapp
from flask import json
import os
cache_http = 'http://localhost:5001'
account_http= 'http://localhost:5002'

@webapp.route('/profile', methods=['GET'])
@login_required
def profile():

    return render_template('profile.html', current_user=current_user)


@webapp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():#done
    if request.method == 'POST':
        key = request.form.get('key')
        new_image = request.files['file']
        username = current_user.username
        #username = request.form.get('username')
        req = {
            'key': key,
            'username': username,
            'value': new_image,
        }
        resp = requests.post(cache_http + '/put', json=req)
        if resp.json() == 'OK':
            return render_template('profile.html', status='Uploaded')
        else:
            return render_template('profile.html', status='Fail to Upload')


@webapp.route('/config', methods=['GET', 'POST'])
@login_required
def config():#done
    if request.method == 'POST':
        capacity = request.form.get('capacity')
        username = current_user.username
       #username = request.form.get('username')
        req = {
            'capacity': capacity,
            'username': username,
        }
        cache_resp = requests.post(cache_http + '/setCap', json=req)
        account_resp = requests.post(account_http + '/updateCapacity', json=req)
        if cache_resp.json() == 'OK' and account_resp.json() == 'UPDATED_CAPACITY':
            return render_template('profile.html', status='Capacity Set')
        else:
            return render_template('profile.html', status='Fail to Set')

@webapp.route('/view_all_image', methods=['GET', 'POST'])
@login_required
def view_all_image():#done
     username = current_user.username
     #username = request.form.get('username')
     req = {
         'username': username,
     }
     resp = requests.post(cache_http + '/showGallery', json=req)
     if resp:
        return render_template('view.html', items=resp)
     else:
        return render_template('view.html')

@webapp.route('/delete_image', methods=['GET', 'POST'])
@login_required
def delete_image():#done
     username = current_user.username
     #username = request.form.get('username')
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
