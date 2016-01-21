#!/usr/bin/python
import os

virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass

from flask import Flask
import logging,sys
import pymongo
from main import app as application

 
if __name__ == '__main__':
    application.run(debug=False)
    logging.basicConfig(stream=sys.stderr)
