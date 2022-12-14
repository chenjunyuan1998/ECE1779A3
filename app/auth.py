import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask import render_template, url_for, request, redirect, flash
from app import webapp
from flask_login import login_required, current_user
from flask import json

from app.profile import cache_http


@webapp.route('/')
def main(): #very first page
    return render_template('login.html')


@webapp.route('/login', methods=['POST'])
def login():

        username = request.form.get('username')
        password =  request.form.get('password')
        remember = True if request.form.get('remember') else False

        if CORRECT_PWD:
            msg = 'Logged in successfully !'
            user = 'username'
            login_user(user, remember=remember)
            #get user info
            return render_template('profile.html', msg=msg, user=user)
        else:
            msg = 'Incorrect username / password !'
            return render_template('login.html', msg=msg)



@webapp.route('/register',methods =['POST'])
def register():
        msg = ''
        username = request.form.get('username')
        password = request.form.get('password')

        if ALREADY_EXISTS:
            msg = 'Account already exists !'
            return render_template('register.html', msg=msg)
        else:
            msg = 'You have successfully registered !'
            return render_template('register.html', msg=msg)


@webapp.route('/logout',methods =['POST'])
def logout():#done
    return redirect(url_for('login'))

@webapp.route('/close_account',methods =['POST'])
def close_account():#done
    username = request.form.get('username')
    req = {
        'username': username,
    }
    resp = requests.post(cache_http + '/deleteUser', json=req)
    if resp.json() == 'OK':
        flash('Delete successfully !')
        return redirect(url_for('login'))
    else:
        msg = 'Fail to delete!'
        return render_template('profile.html', msg=msg)
