from app.main.models.company import Company
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length, Email, Regexp
from flask_babel import _, lazy_gettext as _l
# from app.auth.models.user import User, Domain


class GetStartedForm(FlaskForm):
    name = StringField(_l('Name'),
                       validators=[DataRequired()])
    email = StringField(_l('Email'),
                        validators=[DataRequired(), Email()])
    phonenumber = StringField(_l('Phone Number'),
                              validators=[DataRequired()])
    companyname = StringField(_l('Company Name'),
                              validators=[DataRequired()])
    domainoutput = StringField(_l('Domain'),
                               validators=[DataRequired(), Regexp(r'^[\w.@+-]+$', message="Spaces are not allowed in domain names")], render_kw={'readonly': True})
    submit = SubmitField(_l('Start Now'))


class LeadForm(FlaskForm):
    fname = StringField(_l('First Name'),
                        validators=[DataRequired()])
    lname = StringField(_l('Last Name'),
                        validators=[DataRequired()])
    org = StringField(_l('Organization Name'),
                      validators=[DataRequired()])
    email = StringField(_l('Email'),
                        validators=[DataRequired(), Email()])
    details = TextAreaField(_l('Details'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))