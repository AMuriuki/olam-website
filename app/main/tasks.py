import os
import json
import uuid
from unicodedata import category
from app import db
from app.auth.models.user import User
from app.main.models.blog import Category, Post
from app.main.models.module import FeatureCategory, Module, ModuleCategory, ModuleFeature, Model

from app.main.utils import blog_articles, blog_categories, feature_categories, get_access_group_assosciations, get_access_groups, get_access_rights, get_features, get_models, get_module_categories, get_modules
from app.models import Group, Access


def deploy_module_categories():
    try:
        # module categories
        module_categories = get_module_categories()
        for module_category in module_categories:
            exists = ModuleCategory.query.filter_by(
                id=module_category['id']).first()
            if not exists:
                module_category = ModuleCategory(
                    id=module_category['id'], name=module_category['name'])
                db.session.add(module_category)
                db.session.commit()
    except Exception as e:
        print(e)


def deploy_modules():
    try:
        # modules
        modules = get_modules()
        for module in modules:
            exists = Module.query.filter_by(id=module['id']).first()
            if not exists:
                module = Module(id=module['id'], technical_name=module['technical_name'], bp_name=module['bp_name'], official_name=module['official_name'], category_id=module['category_id'],
                                author=module['author'], url=module['url'], latest_version=module['latest_version'], published_version=module['published_version'], enable=module['enable'], summary=module['summary'])
                db.session.add(module)
                db.session.commit()
    except Exception as e:
        print(e)


def migrate_features():
    try:
        # feature categories
        categories = feature_categories()
        for category in categories:
            exists = FeatureCategory.query.filter_by(id=category['id']).first()
            if exists:
                pass
            else:
                category = FeatureCategory(
                    id=category['id'], title=category['title'])
                db.session.add(category)
                db.session.commit()

        # features
        features = get_features()
        for feature in features:
            exists = ModuleFeature.query.filter_by(id=feature['id']).first()
            if exists:
                pass
            else:
                feature = ModuleFeature(id=feature['id'], name=feature['name'], description=feature['description'],
                                        feature_category=feature['feature_category'], module_id=feature['module_id'])
                db.session.add(feature)
                db.session.commit()

    except Exception as e:
        print(e)


def post_articles():
    try:
        # categories
        categories = blog_categories()
        for category in categories:
            exists = Category.query.filter_by(id=category['id']).first()
            if exists:
                pass
            else:
                category = Category(
                    id=category['id'], name=category['name'], slug=category['slug'])

                db.session.add(category)
                db.session.commit()

        # articles
        articles = blog_articles()
        for article in articles:
            exists = Post.query.filter_by(id=article['id']).first()
            if exists:
                pass
            else:
                post = Post(id=article['id'], title=article['title'], body_html=article['body_html'],
                            category_id=article['category_id'], is_featured=article['is_featured'])
                db.session.add(post)
                db.session.commit()
    except Exception as e:
        print(e)


def migrate_access_groups():
    try:
        # access groups
        access_groups = get_access_groups()
        for access_group in access_groups:
            exists = Group.query.filter_by(id=access_group['id']).first()
            if not exists:
                access_group = Group(
                    id=str(uuid.uuid4()), name=access_group['name'], module_id=access_group['module_id'], permission=access_group['permission'])
                db.session.add(access_group)
                db.session.commit()
    except Exception as e:
        print(e)


def migrate_access_right():
    try:
        # access rights
        access_rights = get_access_rights()
        for access in access_rights:
            exists = Access.query.filter_by(id=access['id']).first()
            if not exists:
                access = Access(id=str(uuid.uuid4()), name=access['name'], model_id=access['model_id'],
                                read=access['read'], write=access['write'], create=access['create'], delete=access['delete'])
                db.session.add(access)
                db.session.commit()
                print("access right " + str(access.id) + " created.")
    except Exception as e:
        print(e)


def migrate_access_group_assosciations():
    try:
        # group access
        group_access = get_access_group_assosciations()
        for _group_access in group_access:
            group = Group.query.filter_by(
                id=_group_access['group_id']).first()
            access = Access.query.filter_by(
                id=_group_access['access_id']).first()
            group.rights.append(access)
            db.session.commit()
    except Exception as e:
        print(e)


def migrate_models():
    try:
        # models
        models = get_models()
        for model in models:
            exists = Model.query.filter_by(id=model['id']).first()
            if exists:
                pass
            else:
                model = Model(id=model['id'], name=model['name'],
                              description=model['description'], module_id=model['module_id'])
                db.session.add(model)
                db.session.commit()
    except Exception as e:
        print(e)
