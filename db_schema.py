from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_mail import Mail
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import backref
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'  # example configuration
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    stories = db.relationship('Story', back_populates="user")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Story(db.Model):
    __tablename__ = 'story'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    anonymous = db.Column(db.Boolean, nullable=False)
    content = db.Column(db.Text, nullable=False)  # Assuming text content
    title = db.Column(db.String(50), nullable=False)

    user = db.relationship('User', back_populates="stories")

    def __init__(self, userId, anonymous, content, title):
        self.userId = userId
        self.anonymous = anonymous
        self.content = content
        self.title = title

class VolunteerOpportunity(db.Model):
    __tablename__ = 'volunteer_opportunity'
    id = db.Column(db.Integer, primary_key=True)
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)  # Detailed description of the opportunity
    location = db.Column(db.String(255), nullable=False)  # Physical or virtual location of the opportunity
    start_date = db.Column(db.DateTime, nullable=False)  # Start date and time of the opportunity
    end_date = db.Column(db.DateTime, nullable=False)  # End date and time of the opportunity
    is_active = db.Column(db.Boolean, default=True)  # Whether the opportunity is currently active

    organizer = db.relationship('User', back_populates="volunteer_opportunities")

    def __init__(self, organizer_id, title, description, location, start_date, end_date, is_active=True):
        self.organizer_id = organizer_id
        self.title = title
        self.description = description
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = is_active


def dbinit():
    tables = inspect(db.engine).get_table_names()
    if len(tables) > 0:
        return
    db.create_all()  # This will create all tables
    db.session.add(User("Mustafa","mustafamamujee03@gmail.com", "root"))
    db.session.commit()

