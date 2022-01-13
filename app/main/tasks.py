import os
import json
from app import db
from app.main.models.module import FeatureCategory, ModuleFeature

from app.main.utils import feature_categories, get_features


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
