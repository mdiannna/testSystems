from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.script import Manager
# from flask.ext.migrate import Migrate, MigrateCommand
# from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret"

UPLOAD_FOLDER = 'files/uploaded/'
# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['py', 'c', 'cpp', 'h'])

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
manager = Manager(app)


Bootstrap(app)
from app import views, models