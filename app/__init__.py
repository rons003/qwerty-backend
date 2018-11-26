from flask import Flask
from flask_cors import CORS, cross_origin
from flask_mongoengine import MongoEngine
import os

app = Flask(__name__)

GAKKO_BLOCKS_CONFIG = os.environ.get('GAKKO_BLOCKS_CONFIG', '')
if not GAKKO_BLOCKS_CONFIG:
    app.config.from_pyfile('config.cfg')
else:      
    app.config.from_envvar('GAKKO_BLOCKS_CONFIG')

CORS(app)
db = MongoEngine(app)

from app.views.chapter_routes import *
from app.views.challenge_routes import *
from app.views.school_routes import *
from app.views.general_routes import *
from app.views.group_routes import *
from app.views.user_routes import *
from app.views.challenge_save_routes import *
from app.views.chapter_item_routes import *
from app.views.project_routes import *
from app.views.section_routes import *
from app.views.module_routes import *
from app.models import models
from app import forms
