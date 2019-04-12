from flask import Blueprint, request, jsonify, abort
from flask_expects_json import expects_json
from services.Authentication.Login import login
from services.Authentication.Logout import logout

authentication = Blueprint('authentication', __name__)

@authentication.route('/login', methods=['POST'])
@expects_json(login_json_schema)
def login_controller():
    response=login(name=request.json['name'], password=request.json['password'])
    return jsonify(response), 200

@authentication.route('/logout', methods=['POST'])
def logout_controller():
    if not request.headers or not 'token' in request.headers:
        abort(400)
    response=logout(token=request.headers['token'])
    return jsonify(response), 200

login_json_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['name', 'password']
}