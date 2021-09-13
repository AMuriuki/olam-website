from flask.helpers import url_for
from sqlalchemy.orm import backref
from app import db
from datetime import date, datetime
from app.models import PaginatedAPIMixin

CompanyModules = db.Table(
    'CompanyModules',
    db.Column('company_id', db.Integer, db.ForeignKey(
        'company.id'), primary_key=True),
    db.Column('module_id', db.Integer, db.ForeignKey(
        'module.id'), primary_key=True)
)


class Company(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    domain_name = db.Column(db.String(120), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    registered_on = db.Column(db.DateTime, default=datetime.now)
    database_id = db.Column(db.Integer, db.ForeignKey('database.id'))
    modules = db.relationship(
        'Module', secondary=CompanyModules, backref=db.backref('company', lazy='dynamic'), lazy='dynamic')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            # 'last_seen': self.last_seen.isoformat() + 'Z',
            '_links': {
                'self': url_for('api.get_company', id=self.id),
                'modules': url_for('api.get_modules', id=self.id),
            }
        }
        return data

    def from_dict(self, data):
        for field in ['last_seen']:
            if field in data:
                setattr(self, field, data[field])
