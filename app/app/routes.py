from app.app import bp
from flask.templating import render_template
from flask_babel import _, get_locale

from app.main.models.module import FeatureCategory, Module, ModuleFeature


@bp.route("/<app_name>")
def view(app_name):
    app_name = app_name
    if app_name == "crm":
        app_name = app_name.upper()
    else:
        app_name = app_name.capitalize()
    return render_template("application.html", title=_(app_name + " Software | Olam ERP"), app_name=app_name)


@bp.route('/<app_name>/features')
def features(app_name):
    return render_template("features.html", app_name=app_name, title=_(app_name + " Software | Olam ERP"))
