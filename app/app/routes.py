from app.app import bp
from flask.templating import render_template
from flask_babel import _, get_locale


@bp.route("/accounting")
def accounting():
    app_name = "Accounting"
    return render_template("finance/accounting.html", title=_("Accounting Software | Olam ERP"), app_name=app_name)
