from app import create_app, db, cli
from flask import url_for, session
from datetime import datetime
from app.auth.models.user import User
from app.auth.models.user import Role
from app.main.models.module import Module, ModuleCategory
from app.auth.models.access import AccessGroup
from app.main.models.language import Lang
from app.auth.models.partner import Partner
from app.main.models.rule import Rule
from app.main.models.model import ModelAccess
from app.main.models.decimal_precision import DecimalPrecision
from app.main.models.actions import ActionWindow, ActionServer
from app.account.models.account_account_tag import AccountAccountTag
from app.account.models.account_payment_term import AccountPaymentTerm
from app.main.models.sequence import Sequence
from app.mail.models.mail_message_subtype import MailMessageSubtype
from app.account.models.account_payment import AccountPaymentMethod
from app.account.models.account_tax import AccountTaxGroup
from app.account.models.account_incoterm import AccountIncoterm
from app.account.models.account_account import AccountAccountType
from app.main.models.cron import Cron
from app.main.models._property import Property
from flask_migrate import Migrate, upgrade
from app import res_db

app = create_app()
cli.register(app)


# @app.before_request
# def before_request():
#     res_db.defaultdb_request('teleios')
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'user': User}


@app.cli.command()
def fetchmail():
    """Scheduled job for fetching incoming emails."""
    # print(str(datetime.utcnow()), 'Fetching emails')
    # user = User(fname='Alfred')
    # db.session.add(user)
    # db.session.commit()
    # return url_for('fetchmail.fetchmail')
    return "success"


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    res_db.defaultdb_request('teleios')    
    # migrate database to latest revision
    upgrade()

    Role.insert_roles()
    # Partner.insert_partners()
    # User.insert_users()
    ModuleCategory.insert_categories()
    # AccessGroup.seed_access_groups()
    # Lang.seed_language()
    # Rule.seed_rules()
    # ModelAccess.insert_modelaccess()
    # DecimalPrecision.insert_decimalprecision()
    # ActionWindow.insert_actionswindow_data()
    # AccountAccountTag.seed_account_tag()
    # AccountPaymentTerm.seed_account_payment_term()
    # Sequence.seed_sequences()
    # MailMessageSubtype.insert_message_subtypes()
    # AccountPaymentMethod.seed_account_payment_method()
    # AccountTaxGroup.seed_account_tax_groups()
    # Property.insert_properties()
    # ActionServer.insert_server_actions()
    # AccountIncoterm.seed_account_incoterm()
    # AccountAccountType.seed_account_type()
    # Cron.insert_cron_jobs()
    Module.insert_modules()


if __name__ == "__main__":
    app.run()
