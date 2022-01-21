import base64
from datetime import datetime, timedelta
from hashlib import md5
import json
import os
import csv
from time import time
from flask import current_app, url_for, session
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import redis
import rq
from app import db, login_manager
from app.search import add_to_index, remove_from_index, query_index
from app.models import SearchableMixin, PaginatedAPIMixin, Task
from flask_login import UserMixin, current_user
from config import basedir

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.local import LocalProxy


import enum
import logging


class VisitorLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(120), index=True)
    country = db.Column(db.String(10), index=True)
    region = db.Column(db.String(120), index=True)
    city = db.Column(db.String(120), index=True)
    lat = db.Column(db.String(120), index=True)
    lng = db.Column(db.String(120), index=True)
    postalcode = db.Column(db.String(120), index=True)
    geonameid = db.Column(db.String(120), index=True)
    connectionType = db.Column(db.String(120), index=True)
    timezone = db.Column(db.String(120), index=True)


class User(UserMixin, PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    company = db.relationship('Company', backref='user_company', uselist=False)
    is_active = db.Column(db.Boolean, default=True)
    name = db.Column(db.String(128), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    is_staff = db.Column(db.Boolean, default=True)
    last_seen = db.Column(db.DateTime, default=datetime.now)
    registered_on = db.Column(db.DateTime, default=datetime.now)
    phone_no = db.Column(db.String(120), index=True)
    tasks = db.relationship('Task', backref='user', lazy='dynamic')
    password_hash = db.Column(db.String(128))
    country_code = db.Column(db.String(10), index=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    def get_database_activation_token(self, expires_in=14400):
        return jwt.encode(
            {'activate_database': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    def get_server_activation_token(self, expires_in=14400):
        return jwt.encode(
            {'activate_server': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    @staticmethod
    def verify_database_activation_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['activate_database']
        except:
            return
        return User.query.get(id)

    @staticmethod
    def verify_server_activation_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['activate_server']
        except:
            return
        return User.query.get(id)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'token': self.name,
            'token_expiration': self.token_expiration,
            'is_active': self.is_active,
            'name': self.name,
            'last_seen': self.last_seen.isoformat() + 'Z',
            'registered_on': self.registered_on.isoformat() + 'Z',
            'is_staff': self.is_staff,
            '_links': {
                'self': url_for('api.get_user', id=self.id)
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['name', 'email', 'token', 'token_expiration', 'company_id']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def get_token(self, expires_in=3600):
        now = datetime.now()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.now() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.now():
            return None
        return user

    def launch_task(self, name, description, *args, **kwargs):
        rq_job = current_app.task_queue.enqueue('app.tasks.' + name, *args, **kwargs)
        task = Task(id=rq_job.get_id(), name=name,
                    description=description, user=self)
        db.session.add(task)
        return task

    def get_tasks_in_progress(self):
        return Task.query.filter_by(user=self, complete=False).all()
    
    def get_completed_task(self, name):
        return Task.query.filter_by(name=name, user=self, complete=True).order_by(Task.id.desc()).first()

    def task_in_progress(self, name):
        return True if Task.query.filter_by(name=name, user=self, complete=False).first() else False
    
    def get_task_in_progress(self, name):
        return Task.query.filter_by(name=name, user=self, complete=False).first()


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
