from flask import jsonify, request, url_for, abort
from app import db
from app import api
from app.main.models.company import Company
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request


@bp.route('/company/<int:id>', methods=['GET'])
@token_auth.login_required
def get_company(id):
    return jsonify(Company.query.get_or_404(id).to_dict())


@bp.route('/companies', methods=['GET'])
@token_auth.login_required
def get_companies():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Company.to_collection_dict(
        Company.query, page, per_page, 'api.get_companies')
    return jsonify(data)


@bp.route('/companies/<int:id>/modules', methods=['GET'])
@token_auth.login_required
def get_modules(id):
    company = Company.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Company.to_collection_dict(
        company.modules, page, per_page, 'api.get_modules', id=id)
    return jsonify(data)


