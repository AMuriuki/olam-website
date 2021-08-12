from app.auth.models.user import User
from app.main.utils import search_dict
from app.main.models.module import Module, ModuleCategory
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app, session, request, abort
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
from app.main import bp
from app.main.forms import GetStartedForm
from config import basedir
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title=_('Tools to Grow Your Business | Olam ERP'))


def onboarding(email, name, domainname, company_name, phonenumber):
    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(name=name, email=email, phone=phonenumber)


@bp.route('/new/database', methods=['GET', 'POST'])
def choose_apps():
    errors = False
    form = GetStartedForm()
    module_categories = ModuleCategory.query.join(
        Module, ModuleCategory.id == Module.category_id).filter(Module.enable.is_(True)).all()
    modules = Module.query.filter(Module.enable.is_(True)).all()

    if form.validate_on_submit():
        domain_name = (form.domainoutput.data).replace(
            '.olam-erp.com', '')  # -> *.olam-erp.com
        session['domain'] = domain_name
        onboarding(form.email.data, form.name.data,
                   domain_name, form.companyname.data, form.phonenumber.data)
        return redirect(url_for('main.home'))
    if form.errors:
        errors = True
    return render_template('main/set-up.html', title=_('New Database | Olam ERP'), form=form, moduleCategories=module_categories, modules=modules, errors=errors)


@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('main/dashboard.html', title=_('Dashboard | Olam ERP'))


@bp.route('/all-apps', methods=['GET', 'POST'])
@login_required
def all_apps():
    return render_template('main/apps.html', title=_('All Apps | Olam ERP'))


@bp.route('/selected_modules', methods=['GET', 'POST'])
def selected_modules():
    if request.method == "POST":
        session['selected_modules'] = request.form.getlist(
            'selected_modules[]')
        return jsonify({"response": "success"})


@bp.route('/home', methods=['GET', 'POST'])
# @login_required
def home():
    return render_template('main/home.html', title=_('Home | Olam ERP'))
