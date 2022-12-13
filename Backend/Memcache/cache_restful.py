from Backend.Memcache import cache_global, webapp

from flask import request
import json

def get_response(input = False):
    if input:
        response = webapp.response_class(
            response = json.dumps('OK'),
            status = 200,
            mimetypes = 'application/json'
        )
    else:
        response = webapp.response_class(
            response = json.dumps('Bad Request'),
            status = 400,
            mimetypes = 'application/json'
        )


@webapp.route('/put', methods = ['POST'])
def put():
    req = request.get_json(force = True)
    username, key, value = list(req.items())[0]
    cache_global.cache.put_key(username,key,value)
    return get_response(True)

@webapp.route('/get', methods = ['POST'])
def get():
    req = request.get_json(force=True)
    username = req["username"]
    key = req["key"]
    response=cache_global.cache.get_key(username,key)
    if response is None:
        return "Unknown key"
    else:
        return response

@webapp.route('/setCap', methods = ['POST'])
def refresh_configs():
    print("In the Route")
    req = request.get_json(force=True)
    username = req['username']
    cap = req['capacity']
    cache_global.cache.set_cap(username , cap)
    return get_response(True)

@webapp.route('/deleteValue', methods = ['POST'])
def delete():
    req = request.get_json(force=True)
    username = req['username']
    key = req['key']
    cache_global.cache.deleteValue(username, key)
    return get_response(True)

@webapp.route('/deleteUser', methods = ['POST'])
def delete():
    req = request.get_json(force=True)
    username = req['username']
    cache_global.cache.delete_user(username)
    return get_response(True)