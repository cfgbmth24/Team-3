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

#Login manager

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

#Mail manager

app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = False  
app.config['MAIL_USERNAME'] = None 
app.config['MAIL_PASSWORD'] = None 
app.config['MAIL_SUPPRESS_SEND'] = False


from flask_mail import Mail, Message
from flask import Flask, request, redirect, url_for, render_template, flash
from itsdangerous import URLSafeTimedSerializer as safeURL

mail = Mail(app)

@app.route("/")
def index():
   return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)