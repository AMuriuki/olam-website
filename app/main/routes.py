from app.auth.email import send_database_activation_email
import re
import time
from os import fsync
from app.main.models.database import Database
from app.main.models.company import Company
from app.auth.models.user import User
from app.main.utils import search_dict, updating
from app.main.models.module import Module, ModuleCategory
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app, session, request, abort
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db, call_ansible
from app.main import bp
from app.main.forms import GetStartedForm
from config import basedir
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title=_('Tools to Grow Your Business | Olam ERP'))


@bp.route('/email_template', methods=['GET', 'POST'])
def email_template():
    return render_template('email/activate_database.html', title=_('Tools to Grow Your Business | Olam ERP'))


def generate_unique_domainname(domain_name):
    if (domain_name[-1].isdigit()):
        int_value = int(domain_name[-1])
        domain_name = domain_name + str(int_value + 1)
    else:
        domain_name = domain_name + "1"
    return domain_name


def onboarding(email, name, domain_name, company_name, phonenumber):
    user = User.query.filter_by(email=email).first()
    company = Company.query.filter_by(domain_name=domain_name).first()
    if user is None:
        user = User(name=name, email=email, phone_no=phonenumber)
        db.session.add(user)
        db.session.commit()
    if company is None:
        company = Company(name=company_name, user_id=user.id,
                          domain_name=domain_name)
    else:
        domain_name = generate_unique_domainname(domain_name)
        company = Company(name=company_name, user_id=user.id,
                          domain_name=domain_name)
    database = Database(name=domain_name)
    db.session.add(database)
    db.session.commit()
    db.session.add(company)
    company.database_id = database.id

    send_database_activation_email(user, domain_name)

    # Install selected App(s)
    modules = session['selected_modules']


@ bp.route('/new/database', methods=['GET', 'POST'])
def choose_apps():
    errors = False
    form = GetStartedForm()
    module_categories = ModuleCategory.query.join(
        Module, ModuleCategory.id == Module.category_id).filter(Module.enable.is_(True)).all()
    modules = Module.query.filter(Module.enable.is_(True)).all()

    if form.validate_on_submit():
        domain_name = (form.domainoutput.data).replace(
            '.olam-erp.com', '')  # -> *.olam-erp.com
        onboarding(form.email.data, form.name.data,
                   domain_name, form.companyname.data, form.phonenumber.data)
        vars = ['APP_NAME', 'SOMETHING']
        new_vars = [domain_name, 'ELSE']
        to_update = dict(zip(vars, new_vars))
        updating('/home/amuriuki/projects/olam-ansible/variables.cnf', to_update)
        # results = call_ansible.run_playbook()
        results = 0
        if results == 0:
            flash(
                _('Activatation Pending! Your database expires in 4 hours. Check your email for the activation link'))
            time.sleep(3600)
        return jsonify({"response": "success" if results == 0 else "fail"})
    if form.errors:
        errors = True
    return render_template('main/set-up.html', title=_('New Database | Olam ERP'), form=form, moduleCategories=module_categories, modules=modules, errors=errors)


@bp.route('/activate_database/<token>', methods=['GET', 'POST'])
def activate_database(token):
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@ bp.route('/dashboard')
@ login_required
def dashboard():
    return render_template('main/dashboard.html', title=_('Dashboard | Olam ERP'))


@ bp.route('/all-apps', methods=['GET', 'POST'])
@ login_required
def all_apps():
    return render_template('main/apps.html', title=_('All Apps | Olam ERP'))


@ bp.route('/selected_modules', methods=['GET', 'POST'])
def selected_modules():
    if request.method == "POST":
        session['selected_modules'] = request.form.getlist(
            'selected_modules[]')
        return jsonify({"response": "success"})


@ bp.route('/home', methods=['GET', 'POST'])
# @login_required
def home():

    return render_template('main/home.html', title=_('Home | Olam ERP'))
