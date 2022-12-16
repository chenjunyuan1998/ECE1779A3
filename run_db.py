#!../venv/bin/python

from Backend.DynamoDB import webapp
webapp.run('0.0.0.0', 5001, debug=True, threaded=True)
