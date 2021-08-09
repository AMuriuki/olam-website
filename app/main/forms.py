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
    # domain = StringField(_l('Domain'),
    #                      validators=[DataRequired()])
    domainoutput = StringField(_l('Domain'),
                               validators=[DataRequired(), Regexp(r'^[\w.@+-]+$', message="Spaces are not allowed in domain names")], render_kw={'readonly': True})
    submit = SubmitField(_l('Start Now'))

    # def validate_domainoutput(self, email):
    #     domain = Domain.query.join(User, Domain.user_id == User.id).filter(
    #         User.email == email.data).first()
    #     if domain is not None:
    #         raise ValidationError(_('Please use a different name.'))
