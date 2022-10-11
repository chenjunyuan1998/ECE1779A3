from flask import Flask
from BackendApp import MemCache

global cache

cache = MemCache.MemCache()

