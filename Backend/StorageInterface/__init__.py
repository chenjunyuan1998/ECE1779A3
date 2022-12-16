from flask import Flask

from Backend.StorageInterface.storageHelper import storageInterface
from Backend.StorageInterface.storage_restful import *

webapp = Flask(__name__)
store = storageInterface()
