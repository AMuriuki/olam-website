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
from app.models import SearchableMixin, PaginatedAPIMixin
from flask_login import UserMixin, current_user
from config import basedir

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.local import LocalProxy


import enum
import logging


class User(UserMixin, PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(128), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone_no = db.Column(db.String(120), index=True, unique=True)
