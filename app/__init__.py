from flask import Flask

import BackendApp.MemCache

global memcache

webapp = Flask(__name__)
#webapp.secret_key = 'secret key'
memcache = BackendApp.MemCache.MemCache(12,"LRU")
db = BackendApp.db


from app import main
from app import upload_get
from app import display_statistics
from app import display_key
from app import display_image
from app import config_memcache










