"""This is the init module.

Provides basic cofigurations.
"""
import requests
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #db name and location
db = SQLAlchemy(app) #db initialize
bcrypt = Bcrypt(app) #bcrypt initialize
login_manager = LoginManager(app) #login_manager initialize
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
sched = BackgroundScheduler(daemon=True) #set APPSCHEDULER to BackgroundScheduler mode
sched.start() #start APPSCHEDULER

from bakalarka import routes
