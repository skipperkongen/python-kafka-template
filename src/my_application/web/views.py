from flask import Blueprint, jsonify, abort, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token
)

from my_application.web.model import db, Action

ROOT = '/api/v1'

auth_bp = Blueprint('auth', __name__)
action_bp = Blueprint('api', __name__)

@action_bp.route(f'{ROOT}/actions/<int:id>', methods=['GET'])
@jwt_required
def get_action(id):
    action = Action.query.get(id)
    if action is None:
        abort(404)
    else:
        return jsonify({'action': action.serialize()})

@action_bp.route(f'{ROOT}/actions/', methods=['GET'])
@jwt_required
def index():
    return jsonify({'actions': list(map(lambda action: action.serialize(), Action.query.all()))})

@action_bp.route(f'{ROOT}/actions/', methods=['POST'])
@jwt_required
def create_action():
    if not request.json or not 'subject' in request.json or 'action' not in request.json:
        abort(400)
    action = Action(request.json['subject'], request.json['action'])
    db.session.add(action)
    db.session.commit()
    return jsonify({'action': action.serialize()}), 201

@action_bp.route(f'{ROOT}/actions/<int:action_id>', methods=['DELETE'])
@jwt_required
def delete_action(id):
    db.session.delete(Action.query.get(id))
    db.session.commit()
    return jsonify({'result': True})


@auth_bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200
