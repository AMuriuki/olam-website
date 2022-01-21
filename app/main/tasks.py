import os
import json
from unicodedata import category
from app import db
from app.main.models.blog import Category, Post
from app.main.models.module import FeatureCategory, ModuleFeature

from app.main.utils import blog_articles, blog_categories, feature_categories, get_features


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
                            author_id=article['author_id'], category_id=article['category_id'], is_featured=article['is_featured'])
                db.session.add(post)
                db.session.commit()
    except Exception as e:
        pass
