from flask import Flask

from Backend.StorageInterface.storageHelper import *
from Backend.StorageInterface.storage_restful import *

webapp = Flask(__name__)
store = storageInterface()
