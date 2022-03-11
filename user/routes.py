from flask import Blueprint
from flask import jsonify
from flask import request
from werkzeug.security import generate_password_hash

from models import User
from models import db

user_blueprint = Blueprint('user_api_routes', __name__, url_prefix='/api/user')


@user_blueprint.route('/all', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    users = [user.serialize() for user in all_users]

    response = {'message': 'Returning all users', 'data': users}
    return jsonify(response)


@user_blueprint.route('/create', methods=['POST'])
def create_user():
    try:
        user = User()
        user.username = request.form['username']
        user.password = generate_password_hash(request.form['password'], method='sha256')

        user.is_admin = True  # In production the is_admin property must be False
        db.session.add(user)
        db.session.commit()

        response = {'message': 'User created', 'data': user.serialize()}
    except Exception as e:
        print(f'Create user error: {e}')
        response = {'message': 'User create error'}

    return jsonify(response)
