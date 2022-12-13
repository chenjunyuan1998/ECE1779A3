from apscheduler.schedulers.background import BackgroundScheduler
from flask import render_template, url_for, request, redirect
from app import webapp
from flask_login import login_required, current_user
from flask import json


@webapp.route('/')
def main(): #very first page
    return render_template('login.html')


@webapp.route('/login', methods=['POST'])
def login():

        username = request.form.get('username')
        password =  request.form.get('password')

        if CORRECT_PWD:
            msg = 'Logged in successfully !'
            user = 'username'
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
def logout():
    return render_template('login.html')

@webapp.route('/close_account',methods =['POST'])
def close_account():
    username = request.form.get('username')
    password = request.form.get('password')

    if DELETED_USER:
        msg = 'Delete successfully !'
        return render_template('login.html', msg=msg)
    else:
        msg = 'Fail to delete!'
        return render_template('profile.html', msg=msg)
