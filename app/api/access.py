from flask import jsonify, request, url_for, abort
from app import db
from app.auth.models.user import User
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import Group, Access
import uuid


@bp.route('/groups/<string:id>', methods=['GET'])
@token_auth.login_required
def get_group(id):
    return jsonify(Group.query.get_or_404(id).to_dict())


@bp.route('/group', methods=['POST'])
def create_group():
    data = request.get_json() or {}
    if 'name' not in data or 'module_id' not in data or 'permission' not in data:
        return bad_request('must include name, module_id and permission fields')
    group = Group(id=str(uuid.uuid4()))
    group.from_dict(data)
    db.session.add(group)
    db.session.commit()
    response = jsonify(group.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_group', id=group.id)
    return response


@bp.route('/group/<string:id>', methods=['PUT'])
def update_group(id):
    group = Group.query.get_or_404(id)
    data = request.get_json() or {}
    group.from_dict(data)
    db.session.commit()
    return jsonify(group.to_dict())