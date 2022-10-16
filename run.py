#!../venv/bin/python
from app import webapp
#webapp.debug = True
webapp.run('0.0.0.0',5000,debug=False)



