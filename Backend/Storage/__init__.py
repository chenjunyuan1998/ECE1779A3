from flask import Flask

from Backend.Storage.storageHelper import *
from Backend.Storage.storage_restful import *

webapp = Flask(__name__)
store = storageInterface()
