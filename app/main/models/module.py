from flask.helpers import url_for
from sqlalchemy.orm import backref
import os
import csv
from app.main.models.blog import Category
from app.models import PaginatedAPIMixin
from config import basedir
from app import db, current_app
import logging

module_models = db.Table(
    'ModuleModels',
    db.Column('module_id', db.Integer, db.ForeignKey(
        'module.id'), primary_key=True),
    db.Column('model_id', db.Integer, db.ForeignKey('model.id'), primary_key=True))


class ModuleCategory(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    modules = db.relationship('Module', backref='category', lazy='dynamic')

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'links': {
                'modules': url_for('api.get_modulesByCategory', id=self.id),
            }
        }
        return data

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


class Module(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    technical_name = db.Column(db.String(128), index=True)  # technical name
    bp_name = db.Column(db.String(128), index=True)  # blueprint name
    official_name = db.Column(db.String(128), index=True)  # official name
    category_id = db.Column(db.Integer, db.ForeignKey('module_category.id'))
    author = db.Column(db.String(60))
    url = db.Column(db.String(120))
    latest_version = db.Column(db.String(60))
    published_version = db.Column(db.String(60))
    icon = db.Column(db.String(60))  # icon url
    enable = db.Column(db.Boolean, default=True)
    summary = db.Column(db.String(350))
    features = db.relationship(
        'ModuleFeature', backref='module', lazy='dynamic')
    access_groups = db.relationship(
        'Group', backref='module', lazy='dynamic')
    models = db.relationship(
        'Model', backref='module', lazy='dynamic')

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
                        id=i['id'], summary=i['summary'], technical_name=i['technical_name'], bp_name=i['bp_name'], author=i['author'], icon=i['icon'], latest_version=i['latest_version'], official_name=i['official_name'], category_id=i['category_id'])
                    db.session.add(module)
                    db.session.commit()

    def to_dict(self):
        category = ModuleCategory.query.filter_by(id=self.category_id).first()
        data = {
            'id': self.id,
            'technical_name': self.technical_name,
            'bp_name': self.bp_name,
            'official_name': self.official_name,
            'summary': self.summary,
            'published_version': self.published_version,
            'category_id': self.category_id,
            'category_name': category.name,
            'links': {
                'access_groups': url_for('api.get_access_groups', id=self.id),
                'models': url_for('api.get_models', id=self.id)
            }
        }
        return data


class ModuleFeature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), index=True)
    description = db.Column(db.Text())
    feature_category = db.Column(
        db.Integer, db.ForeignKey('feature_category.id'))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))


class FeatureCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    features = db.relationship(
        'ModuleFeature', backref='category', lazy='dynamic')


class Model(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128))
    accessrights = db.relationship('Access', backref='model', lazy='dynamic')
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
        return data
