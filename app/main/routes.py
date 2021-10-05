from ipaddress import ip_address
from app.api import company
import os
from app.auth.email import send_server_activation_email
import re
import time
from os import fsync
from app.main.models.database import Database
from app.main.models.company import Company
from app.auth.models.user import User, VisitorLog
from app.main.utils import search_dict, updating
from app.main.models.module import Module, ModuleCategory
from datetime import datetime
from flask import json, render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app, session, request, abort
from flask_login import current_user, login_required
from flask_babel import _, get_locale
# from guess_language import guess_language
from app import db, create_app
from app.main import bp
from app.main.forms import GetStartedForm
from config import basedir
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse
from flask_simple_geoip import SimpleGeoIP

app = create_app()
simple_geoip = SimpleGeoIP(app)


def traverse_geoipdata(data):
    if 'ip' in data:
        ip_address = data['ip']
    else:
        ip_address = None
    if 'location' in data:
        if 'country' in data['location']:
            country = data['location']['country']
        else:
            country = None
        if 'region' in data['location']:
            region = data['location']['region']
        else:
            city = None
        if 'city' in data['location']:
            city = data['location']['city']
        else:
            city = None
        if 'lat' in data['location']:
            lat = data['location']['lat']
        else:
            lat = None
        if 'lng' in data['location']:
            lng = data['location']['lng']
        else:
            lng = None
        if 'postalcode' in data['location']:
            postalcode = data['location']['postalcode']
        else:
            postalcode = None
        if 'timezone' in data['location']:
            timezone = data['location']['timezone']
        else:
            timezone = None
    else:
        country = None
        region = None

    return ip_address, country, region, city, lat, lng, postalcode, timezone


@bp.route('/', methods=['GET', 'POST'])
def index():
    data = simple_geoip.get_geoip_data()
    traverse_geoipdata(data)
    print(data)
    visitor_log = VisitorLog(ip_address=data['ip'], country=data['location']['country'], region=data['location']['region'], city=data['location']['city'], lat=data['location']
                             ['lat'], lng=data['location']['lng'], postalcode=data['location']['postalCode'], geonameid=geonameId, connectionType=data['as']['connectionType'])
    db.session.add(visitor_log)
    db.session.commit()
    print(data)
    return render_template('index.html', title=_('Tools to Grow Your Business | Olam ERP'))


@bp.route('/email_template', methods=['GET', 'POST'])
def errors():
    return render_template('email/activate_server.html', title=_('Tools to Grow Your Business | Olam ERP'))


@bp.route('/401', methods=['GET', 'POST'])
def email_template():
    return render_template('errors/401.html', title=_('Tools to Grow Your Business | Olam ERP'))


def generate_unique_domainname(domain_name):
    if any(char.isdigit() for char in domain_name):
        string_domain_name = ''.join(
            [i for i in domain_name if not i.isdigit()])
        int_value = int(int(re.search(r'\d+', domain_name).group()))
        domain_name = string_domain_name + str(int_value + 1)
    else:
        domain_name = domain_name + "1"
    return domain_name


def onboarding(email, name, domain_name, company_name, phonenumber):
    user = User.query.filter_by(email=email).first()
    company = Company.query.filter_by(domain_name=domain_name).first()
    if user is None:
        user = User(name=name, email=email, phone_no=phonenumber)
        user.set_password('api_user')
        db.session.add(user)
        db.session.commit()
        login_user(user)
    else:
        login_user(user)
    if company is None:
        company = Company(name=company_name, user_id=user.id,
                          domain_name=domain_name)
    else:
        company = Company.query.filter(
            Company.domain_name.contains(domain_name)).order_by(Company.id.desc()).first()
        domain_name = generate_unique_domainname(company.domain_name)
        company = Company(name=company_name, user_id=user.id,
                          domain_name=domain_name)
    database = Database(name=domain_name)
    db.session.add(database)
    db.session.commit()
    company.database_id = database.id
    db.session.add(company)
    db.session.commit()

    session['user_name'] = user.name
    session['domain_name'] = domain_name
    session['companyname'] = company_name
    session['companyid'] = company.id
    session['useremail'] = user.email
    session['user_phone'] = user.phone_no

    # Get selected App(s)
    modules = session['selected_modules']

    # first add free modules
    module = Module.query.filter_by(technical_name="contacts").first()
    company.modules.append(module)
    db.session.commit()

    for module in modules:
        module = Module.query.filter_by(id=module).first()
        company.modules.append(module)
        db.session.commit()

    vars = ['APP_NAME']
    new_vars = [domain_name]
    to_update = dict(zip(vars, new_vars))
    updating('./automate/variables.cnf', to_update)
    user.launch_task('launch_instance', _('Installing...'))
    db.session.commit()
    while user.get_task_in_progress('launch_instance'):
        pass
    flash(
        _('Activation pending! Your database expires in 4 hours. Check your email (' + email + ') for the activation link'))
    send_server_activation_email(user.id, domain_name)
    return {'user_id': user.id, 'user_name': user.name, 'domain_name': domain_name, 'companyname': company_name, 'companyid': company.id, 'user_email': user.email, 'user_phone': user.phone_no}


@bp.route('/check_task_in_progress', methods=['GET', 'POST'])
def check_task_in_progress():
    if request.method == "POST":
        task_name = request.form['task_name']
        if current_user.is_authenticated:
            if current_user.get_task_in_progress(task_name):
                pass
            else:
                return jsonify({"response": "success", "username": session['user_name'], "domainname": session['domain_name'], "companyname": session['companyname'], "companyid": session['companyid'], "useremail": session['user_email'], "userphone": session['user_phone']})
        return jsonify({'response': 'nothing'})


@bp.route('/new/database', methods=['GET', 'POST'])
def choose_apps():
    installing = False
    if current_user.is_authenticated:
        if current_user.get_task_in_progress('launch_instance'):
            installing = True
        else:
            installing = False
    errors = False

    form = GetStartedForm()
    module_categories = ModuleCategory.query.join(
        Module, ModuleCategory.id == Module.category_id).filter(Module.enable.is_(True)).all()
    modules = Module.query.filter(Module.enable.is_(True)).all()

    if form.validate_on_submit():
        domain_name = (form.domainoutput.data).replace(
            '.olam-erp.com', '')  # -> *.olam-erp.com
        response = onboarding(form.email.data, form.name.data,
                              domain_name, form.companyname.data, form.phonenumber.data)
        return jsonify({"response": "success", "username": response['user_name'], "domainname": response['domain_name'], "companyname": response['companyname'], "companyid": response['companyid'], "useremail": response['user_email'], "userphone": response['user_phone']})
    if form.errors:
        errors = True
    return render_template('main/set-up.html', title=_('New Database | Olam ERP'), form=form, moduleCategories=module_categories, modules=modules, errors=errors, installing=installing)


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


@bp.route('/activate_server/<token>', methods=['GET', 'POST'])
def activate_server(token):
    user = User.verify_server_activation_token(token)
    if not user:
        abort(401)
    else:
        company = Company.query.filter_by(
            user_id=user.id).order_by(Company.id.desc()).first()
        database = Database.query.filter_by(
            name=company.domain_name).first()
        database.is_activated = True
        db.session.commit()
        # return redirect("https://" + company.domain_name + ".olam-erp.com/auth/set_password?username=" + user.name + "&companyname=" + company.name + "&companyid=" + company.id + "&domainname=" + company.domain_name + "&email=" + user.email + "&phone_no=" + user.phone_no)
        return redirect("https://127.0.0.1:5000/auth/set_password?username=" + user.name + "&companyname=" + company.name + "&companyid=" + company.id + "&domainname=" + company.domain_name + "&email=" + user.email + "&phone_no=" + user.phone_no)
