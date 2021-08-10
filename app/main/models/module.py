import enum
import os
import csv
from config import basedir
from app import db, current_app
import logging


class StateEnum(enum.Enum):
    uninstallable = 'Uninstallable'
    uninstalled = 'Not Installed'
    installed = 'Installed'
    to_upgrade = 'To be upgraded'
    to_remove = 'To be removed'
    to_install = 'To be installed'


class ModuleCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text)
    visible = db.Column(db.Boolean, default=True)
    sequence = db.Column(db.Integer, index=True)
    modules = db.relationship('Module', backref='category', lazy='dynamic')
    parent_id = db.Column(db.Integer, db.ForeignKey('module_category.id'))
    children = db.relationship('ModuleCategory',
                               backref=db.backref('parent', remote_side=[id])
                               )

    @staticmethod
    def insert_categories():
        csv_file = os.path.join(
            basedir, 'app/main/data/module_category.csv')
        with open(csv_file, 'r') as fin:
            dr = csv.DictReader(fin)
            if 'sqlite' in current_app.config['SQLALCHEMY_DATABASE_URI']:
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
    name = db.Column(db.String(128), index=True)  # technical name
    category_id = db.Column(db.Integer, db.ForeignKey('module_category.id'))
    shortdesc = db.Column(db.String(60))  # module name
    summary = db.Column(db.String(120))
    description = db.Column(db.Text)
    description_html = db.Column(db.Text)
    author = db.Column(db.String(60))
    maintainer = db.Column(db.String(60))
    contributors = db.Column(db.Text)
    website = db.Column(db.String(120))

    # attention: Incorrect field names !!
    #   installed_version refers the latest version (the one on disk)
    #   latest_version refers the installed version (the one in database)
    #   published_version refers the version available on the repository

    installed_version = db.Column(db.String(60))
    latest_version = db.Column(db.String(60))
    published_version = db.Column(db.String(60))

    url = db.Column(db.String(60))
    sequence = db.Column(db.Integer, default=100)
    # dependencies_id = fields.One2many('ir.module.module.dependency', 'module_id',
    #                                    string='Dependencies', readonly=True)

    # exclusion_ids = fields.One2many('ir.module.module.exclusion', 'module_id',
    #                                 string='Exclusions', readonly=True)

    # An auto-installable module is automatically installed by the '
    auto_install = db.Column(db.Boolean, default=False)
    # 'system when all its dependencies are satisfied. '
    # 'If the module has no dependency, it is always installed.

    state = db.Column(
        db.Enum(StateEnum),
        default=StateEnum.uninstallable,
        index=True
    )
    demo = db.Column(db.Boolean, default=False)  # Demo Data
    menus_by_module = db.Column(db.Text)  # menus
    reports_by_module = db.Column(db.Text)  # reports
    views_by_module = db.Column(db.Text)  # views
    application = db.Column(db.Boolean)  # application
    icon = db.Column(db.String(60))  # icon url
    icon_image = db.Column(db.String(120))
    to_buy = db.Column(db.Boolean, default=False)  # Teleios Enterprise Module
    has_iap = db.Column(db.Boolean, default=False)
    enable = db.Column(db.Boolean, default=True)
    web = db.Column(db.Boolean, default=True)
    # company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    @staticmethod
    def insert_modules():
        csv_file = os.path.join(
            basedir, 'app/main/data/modules.csv')
        with open(csv_file, 'r') as fin:
            dr = csv.DictReader(fin)
            if 'sqlite' in current_app.config['SQLALCHEMY_DATABASE_URI']:
                current_app.logger.setLevel(logging.INFO)
                current_app.logger.info('seeding modules table')
                for i in dr:
                    exists = db.session.query(
                        Module.id).filter_by(id=i['id']).first() is not None
                    if exists:
                        pass
                    else:
                        module = Module(
                            id=i['id'], website=i['website'], summary=i['summary'], name=i['name'], author=i['author'], icon=i['icon'], state=i['state'], latest_version=i['latest_version'], shortdesc=i['shortdesc'], category_id=i['category_id'], application=True if i['application'] == 't' else False, demo=True if i['demo'] == 't' else False, web=True if i['web'] == 't' else False, sequence=i['sequence'], auto_install=True if i['auto_install'] == 't' else False, to_buy=True if i['to_buy'] == 't' else False, description=i['description'])
                        db.session.add(module)
                    db.session.commit()
