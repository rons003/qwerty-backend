#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.append("var/www/code-gakko-app-backend/")

from app import app as application
application.secret_key = 'Add your secret key'
