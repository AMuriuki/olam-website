from app.main.models.module import Module, ModuleCategory
import os
import click
from flask_migrate import upgrade

from app.main.tasks import deploy_module_categories, deploy_modules, migrate_access_group_assosciations, migrate_access_groups, migrate_access_right, migrate_features, migrate_models, post_articles


def register(app):
    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

    @app.cli.command()
    def deploy():
        """Run deployment tasks."""
        # migrate database to latest revision
        upgrade()
        deploy_module_categories()
        deploy_modules()
        migrate_access_groups()
        migrate_models()
        migrate_access_right()
        # migrate_features()
        # post_articles()
        # migrate_access_group_assosciations()

    @translate.command()
    @click.argument('lang')
    def init(lang):
        """Initialize a new language."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system(
                'pybabel init -i messages.pot -d app/translations -l ' + lang):
            raise RuntimeError('init command failed')
        os.remove('messages.pot')

    @translate.command()
    def update():
        """Update all languages."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system('pybabel update -i messages.pot -d app/translations'):
            raise RuntimeError('update command failed')
        os.remove('messages.pot')

    @translate.command()
    def compile():
        """Compile all languages."""
        if os.system('pybabel compile -d app/translations'):
            raise RuntimeError('compile command failed')
