# create the Flask app
import re
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

import os

from flask import make_response, render_template_string
from flask import session

app.secret_key="is nothing secret"

from werkzeug import security
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask import flash
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash

#Database manager

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///eventsite.sqlite'

from db_schema import db, User, Story, Charity, TypeLookup, dbinit

db.init_app(app)

with app.app_context():
  dbinit()



