from app.app import bp
from flask.templating import render_template
from flask_babel import _, get_locale


@bp.route("/<app_name>")
def view(app_name):
    app_name = app_name
    return render_template("finance/accounting.html", title=_("Accounting Software | Olam ERP"), app_name=app_name)


@bp.route('/<app_name>/features')
def features(app_name):
    if app_name:
        app_name = app_name
    else:
        app_name = None
    return render_template("features.html", app_name=app_name, title=_("Olam " + app_name + " | Olam ERP"))
