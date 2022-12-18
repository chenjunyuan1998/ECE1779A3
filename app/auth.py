import profile

import requests
from flask import render_template, url_for, request, redirect, make_response,flash
from app import webapp
from flask import json

cache_http = 'http://localhost:5002'
account_http= 'http://localhost:5001'


@webapp.route('/')
def main(): #very first page
    return render_template('login.html')


@webapp.route('/login_get', methods=['POST'])
def login_get():#done
    return render_template('login.html')


@webapp.route('/login', methods=['POST'])
def login():#done

        username = request.form.get('username')
        password =  request.form.get('password')
        #remember = True if request.form.get('remember') else False

        req = {
            'username': username,
            'password': password,
        }
        resp = requests.post(account_http + '/signIn', json=req)
        print("resp.json(): ", resp.json())
        if resp.json() == 'CORRECT_PWD':
            msg = 'Logged in successfully !'
            resp_space = requests.get(cache_http + '/showSpaceUsed', json=req)
            print('resp_space auth:', resp_space)
            print('resp_space.json() auth:', resp_space.json())
            resp1 = make_response(render_template('profile.html', user=username, space=resp_space.json()))
            resp1.set_cookie('username', username)
            return resp1
        elif resp.json() == 'INCORRECT_PWD':
            msg = 'Incorrect password !'
            return render_template('login.html', msg=msg)
        else:
            msg = 'Invalid user!'
            return render_template('login.html', msg=msg)


@webapp.route('/register', methods=['POST'])
def register():#done
        username = request.form.get('username')
        password = request.form.get('password')
        req = {
            'username': username,
            'password': password,
        }
        account_resp = requests.post(account_http + '/signUp', json=req)
        # cache_resp = requests.post(cache_http + '/addUser', json=req)
        if account_resp.json() == 'ALREADY_EXISTS':
            msg = 'Account already exists !'
            return render_template('register.html', msg=msg)
        elif account_resp.json() == 'INVALID_NAME':
            msg = 'Invalid Username !'
            return render_template('register.html', msg=msg)
        else:
            msg = 'You have create an account !'
            return render_template('register.html', msg=msg)


@webapp.route('/register_get', methods=['GET', 'POST'])
def register_get():#done
    return render_template('register.html')


@webapp.route('/logout', methods=['POST'])
def logout():#done
    return redirect(url_for('login_get'))


@webapp.route('/close_account', methods=['POST'])
#@login_required
def close_account():#done
    username = request.cookies.get('username')
    password = request.form.get('password')
    req = {
        'username': username,
        'password': password,
    }
    cache_resp = requests.post(cache_http + '/deleteUser', json=req)
    account_resp = requests.post(account_http + '/closeAccount', json=req)
    if cache_resp.json() == 'OK' and account_resp.json() == 'DELETED_USER':
        # flash('Delete successfully !')
        return redirect(url_for('login_get'))
    else:
        msg = 'Fail to delete!'
        resp_space = requests.get(cache_http + '/showSpaceUsed', json=req)
        return render_template('profile.html', msg=msg, user=username, space=resp_space.json())
