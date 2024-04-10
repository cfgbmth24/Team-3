from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_mail import Mail
from flask_login import UserMixin
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import backref
from datetime import datetime, timedelta

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)  # Use 'id' to comply with Flask-Login's expectations
    name = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    verified = db.Column(db.Boolean, nullable=False)

    typeUser = db.Column(db.Integer,db.ForeignKey('typelookup.id'), nullable=False)
    charityId = db.Column(db.Integr, db.ForeignKey('charity.id'), nullable=True)

    typeuser = db.relationship('TypeLookup', back_populates="user")
    charity = db.relationship('Charity', back_populates="user")
    story = db.relationship('Story', back_populates = "user")


    def __init__(self,name, email, password, verified):
        self.name = name
        self.email = email
        self.set_password(password)
        self.verified = verified

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def check_verified(self):
        return self.verified
    
class Story(db.Model):
    __tablename__ = 'story'
    id = db.Column(db.Integer, primary_key=True)  # Use 'id' to comply with Flask-Login's expectations
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    anonymous = db.Column(db.Boolean, nullable=False)
    content = db.Column(db.Blob, nullable=False)
    title = db.Column(db.String(50), nullable=False)

    user = db.relationship('User', back_populates="story")

    def __init__(self, userId, anonymous, content, title):
        self.userId = userId
        self.anonymous = anonymous
        self.content = content
        self.title = title

class Charity(db.Model):
    __tablename__ = 'charity'
    id = db.Column(db.Integer, primary_key=True)  # Use 'id' to comply with Flask-Login's expectations
    name = db.Column(db.Sting(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Blob, nullable=False)

    user = db.relationship('User', back_populates="charity")

    def __init__(self,name, location, description):
        self.name = name
        self.location = location
        self.description = description

class TypeLookup(db.Model):
    __tablename__ = 'typelookup'
    id = db.Column(db.Integer, primary_key=True)
    userType = db.Column(db.String(40), nullable=False)

    def __init__(self, typeId, userType):
        self.id = typeId
        self.userType = userType


def dbinit():
    tables = inspect(db.engine).get_table_names()
    if len(tables) > 0:
        return
    db.create_all()