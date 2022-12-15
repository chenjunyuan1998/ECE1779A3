import profile

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask import render_template, url_for, request, redirect, flash
from app import webapp
from flask_login import login_user, logout_user, login_required, current_user
from flask import json

cache_http = 'http://localhost:5001'
account_http= 'http://localhost:5002'

@webapp.route('/')
def main(): #very first page
    return render_template('login.html')


@webapp.route('/login', methods=['POST'])
def login():#done

        username = request.form.get('username')
        password =  request.form.get('password')
        remember = True if request.form.get('remember') else False

        req = {
            'username': username,
            'password': password,
        }
        resp = requests.post(account_http + '/signIn', json=req)
        if resp.json() == 'CORRECT_PWD':
            msg = 'Logged in successfully !'
            user = get_user(username)
            login_user(user, remember=remember)
            return redirect(url_for('profile.profile'))
        elif resp.json() == 'INCORRECT_PWD':
            msg = 'Incorrect password !'
            return render_template('login.html', msg=msg)
        else:
            msg = 'Invalid user!'
            return render_template('login.html', msg=msg)



@webapp.route('/register',methods =['POST'])
def register():#done

        username = request.form.get('username')
        password = request.form.get('password')
        req = {
            'username': username,
            'password': password,
        }
        resp = requests.post(account_http + '/signUp', json=req)
        if resp.json() == 'ALREADY_EXISTS':
            msg = 'Account already exists !'
            return render_template('register.html', msg=msg)
        elif resp.json() == 'INVALID_NAME':
            msg = 'Invalid Username !'
            return render_template('register.html', msg=msg)
        else:
            msg = 'You have create an account !'
            return render_template('register.html', msg=msg)


@webapp.route('/logout',methods =['POST'])
def logout():#done
    return redirect(url_for('login'))

@webapp.route('/close_account',methods =['POST'])
@login_required
def close_account():#done
    username = current_user.username
    password = current_user.password
    #username = request.form.get('username')
    req = {
        'username': username,
        'password': password,
    }
    cache_resp = requests.post(cache_http + '/deleteUser', json=req)
    account_resp = requests.post(account_http + '/closeAccount', json=req)
    if cache_resp.json() == 'OK' and account_resp.json() == 'DELETED_USER':
        flash('Delete successfully !')
        return redirect(url_for('login'))
    else:
        msg = 'Fail to delete!'
        return render_template('profile.html', msg=msg)
