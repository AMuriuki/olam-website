from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app, session, request, abort
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
# from app.main.models.module import Module, ModuleCategory
# from app.translate import translate
from app.main import bp
from app.main.forms import GetStartedForm
# from app.decorators import admin_required
# from app.main.models.company import Company
# from app.main.models.module import Module
# from app import res_db
from config import basedir
# from app.auth.models.user import User, Role, Domain
from flask_login import login_user, logout_user, current_user
# from app.auth.email import send_confirmation_email
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse


@bp.route('/', methods=['GET', 'POST'])
def index():
    # subdomain = get_subdomain_value()
    # if subdomain:
    #     domain = Domain.query.filter_by(name=subdomain).first()
    #     if domain is None:
    #         return redirect(url_for('main.domain_not_found', domain=subdomain+'.teleios.com'))
    #     else:
    #         return redirect(url_for('auth.login'))
    return render_template('index.html', title=_('Tools to Grow Your Business | Shalem'))