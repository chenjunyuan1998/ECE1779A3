from flask import Flask

from Backend.Storage.storageHelper import *

webapp = Flask(__name__)
store = storageInterface()

from Backend.Storage.storage_restful import *