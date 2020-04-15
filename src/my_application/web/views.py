from flask import Blueprint, jsonify, abort, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token
)

from my_application.core.db import Session
from my_application.core.models import Action

ROOT = '/api/v1'

auth_bp = Blueprint('auth', __name__)
action_bp = Blueprint('api', __name__)

@action_bp.route(f'{ROOT}/actions/<int:id>', methods=['GET'])
@jwt_required
def get_action(id):
    item = Session.query(Action).get(id)
    if item is None:
        abort(404)
    else:
        return jsonify({'action': item.serialize()})

@action_bp.route(f'{ROOT}/actions/', methods=['GET'])
@jwt_required
def index():
    items = Session.query(Action).all()
    return jsonify({'actions': list(map(lambda action: action.serialize(), items))})

@action_bp.route(f'{ROOT}/actions/', methods=['POST'])
@jwt_required
def create_action():
    if not request.json or not 'subject' in request.json or 'action' not in request.json:
        abort(400)
    subject = request.json['subject']
    action = request.json['action']
    item = Action(subject=subject, action=action)
    Session.add(item)
    Session.commit()
    return jsonify({'action': item.serialize()}), 201

@action_bp.route(f'{ROOT}/actions/<int:action_id>', methods=['DELETE'])
@jwt_required
def delete_action(id):
    item = Session.query(Action).get(id)
    Session.delete(item)
    Session.commit()
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
