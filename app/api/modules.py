from flask import request, jsonify
from app.api import bp
from app.main.models.module import Model, Module, ModuleCategory


@bp.route('/module_categories', methods=['GET'])
def get_modulesCategories():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = ModuleCategory._to_collection_dict(
        ModuleCategory.query.join(
        Module, ModuleCategory.id == Module.category_id), page, per_page, 'api.get_modulesCategories')
    return jsonify(data)


@bp.route('/apps/category/<int:id>', methods=['GET'])
def get_modulesByCategory(id):
    modules_category = ModuleCategory.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = ModuleCategory.to_collection_dict(
        modules_category.modules, page, per_page, 'api.get_apps', id=id)
    print(len(data))
    return jsonify(data)


@bp.route('/apps', methods=['GET'])
def get_apps():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Module._to_collection_dict(
        Module.query, page, per_page, 'api.get_apps')
    return jsonify(data)


@bp.route('/modules', methods=['GET'])
def get_modules():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Module._to_collection_dict(
        Module.query, page, per_page, 'api.get_modules')
    return jsonify(data)


@bp.route('/models', methods=['GET'])
def get_models():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Model._to_collection_dict(
        Model.query, page, per_page, 'api.get_models')
    return jsonify(data)