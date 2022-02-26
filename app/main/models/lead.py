from datetime import datetime
from app import db


class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(128), index=True)
    lname = db.Column(db.String(128), index=True)
    orgname = db.Column(db.String(128), index=True)
    email = db.Column(db.String(128), index=True)
    utm_source = db.Column(db.String(128), index=True)
    utm_medium = db.Column(db.String(128), index=True)
    utm_campaign = db.Column(db.String(128), index=True)
    details = db.Column(db.Text(), index=True)
    creation_date = db.Column(db.DateTime, default=datetime.now)
