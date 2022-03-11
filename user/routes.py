import json
from flask import Blueprint
from flask import jsonify

user_blueprint = Blueprint('user_api_routes', __name__, url_prefix='/api/user')


@user_blueprint.route('/all', methods=['GET'])
def get_all_users():
    return jsonify([])
