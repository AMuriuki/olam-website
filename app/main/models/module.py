from flask.helpers import url_for
from sqlalchemy.orm import backref
from app.main.models.company import CompanyModules
import enum
import os
import csv
from config import basedir
from app import db, current_app
import logging


class ModuleCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    modules = db.relationship('Module', backref='category', lazy='dynamic')

    @staticmethod
    def insert_categories():
        csv_file = os.path.join(
            basedir, 'app/main/data/module_category.csv')
        with open(csv_file, 'r') as fin:
            dr = csv.DictReader(fin)
            current_app.logger.setLevel(logging.INFO)
            current_app.logger.info('seeding module_categories table')
            for i in dr:
                exists = db.session.query(
                    ModuleCategory.id).filter_by(id=i['id']).first() is not None
                if exists:
                    pass
                else:
                    category = ModuleCategory(
                        id=i['id'], name=i['name'])
                    db.session.add(category)
                    db.session.commit()


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    technical_name = db.Column(db.String(128), index=True)  # technical name
    official_name = db.Column(db.String(128), index=True)  # technical name
    category_id = db.Column(db.Integer, db.ForeignKey('module_category.id'))
    author = db.Column(db.String(60))
    url = db.Column(db.String(120))
    installed_version = db.Column(db.String(60))
    latest_version = db.Column(db.String(60))
    published_version = db.Column(db.String(60))
    auto_install = db.Column(db.Boolean, default=False)
    state = db.Column(db.String(60))
    icon = db.Column(db.String(60))  # icon url
    enable = db.Column(db.Boolean, default=True)
    summary = db.Column(db.String(350))
    # companies = db.relationship(
    #     'Company', secondary=CompanyModules, backref='module')

    @staticmethod
    def insert_modules():
        csv_file = os.path.join(
            basedir, 'app/main/data/modules.csv')
        with open(csv_file, 'r', encoding='mac_roman', newline='') as fin:
            dr = csv.DictReader(fin)
            current_app.logger.setLevel(logging.INFO)
            current_app.logger.info('seeding modules table')
            for i in dr:
                exists = db.session.query(
                    Module.id).filter_by(id=i['id']).first() is not None
                if exists:
                    pass
                else:
                    module = Module(
                        id=i['id'], summary=i['summary'], technical_name=i['technical_name'], author=i['author'], icon=i['icon'], state=i['state'], latest_version=i['latest_version'], official_name=i['official_name'], category_id=i['category_id'], auto_install=True if i['auto_install'] == 't' else False, enable=True if i['enable'] == 't' else False)
                    db.session.add(module)
                    db.session.commit()

    def to_dict(self):
        data = {
            'id': self.id,
            'technical_name': self.technical_name,
            'official_name': self.official_name,
            '_links': {
                'self': url_for('api.get_modules', id=self.id),
                # 'category': url_for('api.get_category', id=self.id),
            }
        }
        return data
