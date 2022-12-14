from flask import Flask

from Backend.Memcache.cache import Cache

webapp = Flask(__name__)
cache = Cache()
