from flask import jsonify, request, url_for, abort
from app import db
from app import api
from app.main.models.company import Company
from app.main.models.module import Module
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import Group


@bp.route('/company/<int:id>', methods=['GET'])
@token_auth.login_required
def get_company(id):
    return jsonify(Company.query.get_or_404(id).to_dict())


@bp.route('/companies', methods=['GET'])
def get_companies():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Company.to_collection_dict(
        Company.query, page, per_page, 'api.get_companies')
    return jsonify(data)


@bp.route('/companies/<int:id>/modules', methods=['GET'])
def get_modules(id):
    company = Company.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Company.to_collection_dict(
        company.modules, page, per_page, 'api.get_modules', id=id)
    print(len(data))
    return jsonify(data)


@bp.route('/modules/<int:id>/access_groups', methods=['GET'])
def get_access_groups(id):
    module = Module.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Module.to_collection_dict(
        module.access_groups, page, per_page, 'api.get_access_groups', id=id)
    print(len(data))
    return jsonify(data)


@bp.route('/access_groups/<string:id>/access_rights', methods=['GET'])
def get_access_rights(id):
    access_group = Group.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Group._to_collection_dict(
        access_group.rights, page, per_page, 'api.get_access_rights', id=id)
    return jsonify(data)


@bp.route('/modules/<int:id>/models', methods=['GET', 'POST'])
def get_models(id):
    module = Module.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Module._to_collection_dict(
        module.models, page, per_page, 'api.get_models', id=id)
    return jsonify(data)
