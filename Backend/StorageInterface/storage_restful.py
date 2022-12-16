from Backend.StorageInterface import store_global, webapp

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
    key, username, value = list(req.items())[0]
    store_global.store.put_key(username, key, value)
    return get_response(True)

@webapp.route('/get', methods = ['POST'])
def get():
    req = request.get_json(force=True)
    username = req["username"]
    key = req["key"]
    response=store_global.store.get_key(username, key)
    if not response:
        return "Unknown key"
    else:
        return response

@webapp.route('/setCap', methods = ['POST'])
def setCap():
    print("In the Route")
    req = request.get_json(force=True)
    username = req['username']
    cap = req['capacity']
    store_global.store.set_cap(username, cap)
    return get_response(True)

@webapp.route('/deleteValue', methods = ['POST'])
def deleteValue():
    req = request.get_json(force=True)
    username = req['username']
    key = req['key']
    store_global.store.deleteValue(username, key)
    return get_response(True)

@webapp.route('/deleteUser', methods = ['POST'])
def deleteUser():
    req = request.get_json(force=True)
    username = req['username']
    store_global.store.delete_user(username)
    return get_response(True)

@webapp.route('/showGallery', methods = ['POST'])
def showGallery():
    req = request.get_json(force=True)
    username = req["username"]
    response = store_global.store.showGallery(username)
    return response

@webapp.route('/setCapacity', method = ['POST'])
def setCapacity():
    req = request.get_json(force = True)
    username = req["username"]
    store_global.store.set_cap(username)
    return get_response(True)

@webapp.route('/showSpaceUsed', method = ['POST'])
def showSpaceUsed():
    req = request.get_json(force = True)
    username = req["username"]
    store_global.store.showSpaceAllocated(username)
    return get_response(True)
