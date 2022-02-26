from datetime import datetime
from enum import unique
from app import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True, index=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    category_id = db.Column(
        db.Integer, db.ForeignKey('category.id'), nullable=True)
    is_featured = db.Column(db.Boolean, default=False)
    image_url = db.Column(db.Text())


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, index=True)
    slug = db.Column(db.String(120), unique=True, index=True)
    posts = db.relationship('Post', backref='category', lazy='dynamic')
