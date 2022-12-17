from Backend.Storage import store_global, webapp, storageHelper
from Backend.Storage import webapp

from flask import request
import json


def get_response(input=False):
    if input:
        response = webapp.response_class(
            response=json.dumps('OK'),
            status=200,
            mimetype='application/json'
        )
    else:
        response = webapp.response_class(
            response=json.dumps('Bad Request'),
            status=400,
            mimetype='application/json'
        )


@webapp.route('/put', methods=['POST'])
def put():
    req = request.get_json(force=True)
    key = req['key']
    username = req['username']
    value = req['value']
    response = store_global.store.put_key(username, key,value)
    print("put from storage: ", response)
    return json.dumps(response)


@webapp.route('/get', methods=['POST'])
def get():
    req = request.get_json(force=True)
    username = req["username"]
    key = req["key"]
    response = store_global.store.get_key(username, key)
    if not response:
        return json.dumps("Unknown key")
    else:
        return json.dumps(response)


@webapp.route('/setCap', methods=['POST'])
def setCap():
    print("Setting capacity.")
    req = request.get_json(force=True)
    username = req['username']
    cap = req['capacity']
    store_global.store.set_cap(username, cap)
    return get_response(True)


@webapp.route('/deleteValue', methods=['POST'])
def deleteValue():
    req = request.get_json(force=True)
    username = req['username']
    key = req['key']
    response = store_global.store.deleteValue(username, key)
    return json.dumps(response)


@webapp.route('/deleteUser', methods=['POST'])
def deleteUser():
    req = request.get_json(force=True)
    username = req['username']
    store_global.store.delete_user(username)
    return get_response(True)


@webapp.route('/showGallery', methods=['GET'])
def showGallery():
    req = request.get_json(force=True)
    username = req["username"]
    return json.dumps(store_global.store.showGallery(username))


@webapp.route('/showSpaceUsed', methods=['GET'])
def showSpaceUsed():
    req = request.get_json(force=True)
    username = req["username"]
    return json.dumps(store_global.store.showSpaceAllocated(username))


@webapp.route('/addUser', methods=['POST'])
def addUser():
    req = request.get_json(force=True)
    username = req["username"]
    return get_response(True)

def startup_app():
    store_global.store = storageHelper.storageInterface()

startup_app()
