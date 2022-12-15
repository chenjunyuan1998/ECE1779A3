from flask import Flask

from Backend.Memcache.storageHelper import storageInterface

webapp = Flask(__name__)
store = storageInterface()
