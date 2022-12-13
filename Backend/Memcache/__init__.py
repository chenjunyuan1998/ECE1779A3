from flask import Flask

from Backend.Memcache.Cache import Cache

webapp = Flask(__name__)
cache = Cache()
