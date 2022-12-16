from flask import Flask

from Backend.StorageInterface.storageHelper import storageInterface

webapp = Flask(__name__)
store = storageInterface()
