from unittest import result

from flask import Blueprint
from flask import jsonify

from models import User

user_blueprint = Blueprint('user_api_routes', __name__, url_prefix='/api/user')


@user_blueprint.route('/all', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    users = [user.serialize() for user in all_users]

    response = {'message': 'Returning all users', 'data': users}
    return jsonify(response)
