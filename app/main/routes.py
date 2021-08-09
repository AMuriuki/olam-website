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
    return render_template('index.html', title=_('Tools to Grow Your Business | Shalem'))


@bp.route('/new/database', methods=['GET', 'POST'])
def choose_apps():
    form = GetStartedForm()

    if form.validate_on_submit():
        return redirect(url_for('main.home'))
    if form.errors:
        pass
    return render_template('main/set-up.html', title=_('New Database | Shalem'), form=form)


@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('main/dashboard.html', title=_('Dashboard | Shalem'))