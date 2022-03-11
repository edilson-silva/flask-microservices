from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from werkzeug.security import check_password_hash
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


@user_blueprint.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if not user:
        response = {'message': 'User not found'}
        return make_response(jsonify(response), 404)

    if check_password_hash(user.password, password):
        user.update_api_key()
        db.session.commit()
        login_user(user)

        response = {'message': 'Logged in', 'api_key': user.api_key}
        return make_response(jsonify(response), 200)

    response = {'message': 'Access denied'}
    return make_response(jsonify(response), 401)


@user_blueprint.route('logout', methods=['POST'])
def logout():
    if current_user.is_authenticaed:
        logout_user()
        return jsonify({'message': 'Logged in'})

    return jsonify({'message': 'No user logged in'}), 401


@user_blueprint.route('/<username>/exists', methods=['GET'])
def user_exists(username):
    user = User.query.filter_by(username=username).first()

    if user:
        return jsonify({'message': 'User exists'})

    return jsonify({'message': 'User nor exists'}), 404
