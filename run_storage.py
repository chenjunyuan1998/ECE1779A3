#!../venv/bin/python

from Backend.StorageInterface import webapp
webapp.run('0.0.0.0', 5002, debug=True, threaded=True)
