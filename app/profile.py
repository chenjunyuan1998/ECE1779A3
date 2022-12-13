
from flask import render_template, url_for, request, flash, redirect

from app import webapp
from flask import json
import os

@webapp.route('/profile', methods=['GET'])
def profile():
    return render_template('profile.html', user = user)


@webapp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        key = request.form.get('key')
        new_image = request.files['file']
        username = request.form.get('username')
        if UPLOADED:
            return render_template('profile.html', status = 'Uploaded', user = user)
        else:
            return render_template('profile.html', status='Fail to Upload', user=user)


@webapp.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        capacity = request.form.get('capacity')
        username = request.form.get('username')
        if SUCCESS:
            return render_template('profile.html', status = 'Capacity Set', user = user)
        else:
            return render_template('profile.html', status='Fail to Set', user=user)

@webapp.route('/view_all_image', methods=['GET', 'POST'])
def view_all_image():
     username = request.form.get('username')
     return render_template('view.html', user = user, image=image, key=key)

@webapp.route('/delete_image', methods=['GET', 'POST'])
def delete_image():
     username = request.form.get('username')
     key = request.form.get('key')
     return render_template('view.html', user = user, key_mage=key_image)
