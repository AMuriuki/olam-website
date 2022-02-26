from app.app import bp
from flask.templating import render_template
from flask_babel import _, get_locale

from app.main.models.module import FeatureCategory, Module, ModuleFeature


@bp.route("/<app_name>")
def view(app_name):
    app_name = app_name
    return render_template("application.html", title=_("Accounting Software | Olam ERP"), app_name=app_name)


@bp.route('/<app_name>/features')
def features(app_name):
    feature_categories = []
    if app_name:
        app_name = app_name
        module = Module.query.filter_by(bp_name=app_name).first()
        features = ModuleFeature.query.filter_by(
            module_id=module.id).all()
        for feature in features:
            feature_categories.append(feature.feature_category)
        print(feature_categories)
        categories = FeatureCategory.query.filter(
            FeatureCategory.id.in_(feature_categories)).all()
        print(categories)
    else:
        app_name = None
    return render_template("features.html", app_name=app_name, title=_("Olam " + app_name + " | Olam ERP"), features=features, categories=categories)
