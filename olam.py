from flask_migrate import upgrade
from app import create_app, cli, db
from app.main.models.module import Module, ModuleCategory

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db}


@app.context_processor
def modules():
    modules = Module.query.filter(Module.enable.is_(True)).all()
    if modules:
        return dict(modules=modules)
    else:
        return dict(modules="")


@app.context_processor
def module_categories():
    module_categories = ModuleCategory.query.join(
        Module, ModuleCategory.id == Module.category_id).filter(Module.enable.is_(True)).all()

    if module_categories:
        return dict(moduleCategories=module_categories)
    else:
        return dict(moduleCategories="")
