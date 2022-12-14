import requests
from flask import render_template, url_for, request, flash, redirect

from app import webapp
from flask import json
import os
cache_http = 'http://localhost:5001'

@webapp.route('/profile', methods=['GET'])
def profile():
    return render_template('profile.html', user = user)


@webapp.route('/upload', methods=['GET', 'POST'])
def upload():#done
    if request.method == 'POST':
        key = request.form.get('key')
        new_image = request.files['file']
        username = request.form.get('username')
        req = {
            'key': key,
            'username': username,
            'value': new_image,
        }
        resp = requests.post(cache_http + '/put', json=req)
        if resp.json() == 'OK':
            return render_template('profile.html', status='Uploaded', user=user)
        else:
            return render_template('profile.html', status='Fail to Upload', user=user)


@webapp.route('/config', methods=['GET', 'POST'])
def config():#done
    if request.method == 'POST':
        capacity = request.form.get('capacity')
        username = request.form.get('username')
        req = {
            'capacity': capacity,
            'username': username,
        }
        resp = requests.post(cache_http + '/setCap', json=req)
        if resp.json() == 'OK':
            return render_template('profile.html', status='Capacity Set')
        else:
            return render_template('profile.html', status='Fail to Set')

@webapp.route('/view_all_image', methods=['GET', 'POST'])
def view_all_image():#done
     username = request.form.get('username')
     req = {
         'username': username,
     }
     resp = requests.post(cache_http + '/showGallery', json=req)
     if resp:
        return render_template('view.html', items=resp)
     else:
        return render_template('view.html')

@webapp.route('/delete_image', methods=['GET', 'POST'])
def delete_image():#done
     username = request.form.get('username')
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
