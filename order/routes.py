from os import environ
from typing import Dict

import requests
from flask import Blueprint
from flask import jsonify
from flask import request

from models import Order
from models import OrderItem
from models import db

order_blueprint = Blueprint('order_api_routes', __name__, url_prefix='/api/order')

USER_API = environ.get('USER_API')


def get_user(api_key) -> Dict:
    headers = {
        'Authorization': api_key
    }

    response = requests.get(USER_API, headers=headers)

    if not response.ok:
        return {'message': 'User not authorized'}

    user = response.json()
    return user


@order_blueprint.route('/', methods=['GET'])
def get_open_order():
    api_key = request.headers.get('Authorization')

    if not api_key:
        return jsonify({'message': 'Not logged in'}), 401

    response = get_user(api_key)

    user = response.get('data')

    if not user:
        return jsonify({'message': 'User not found'}), 404

    user_id = user['id']

    open_order = Order.query.filter_by(user_id=user_id, is_open=1).first()

    if open_order:
        return jsonify({'data': open_order.serialize()}), 200

    return jsonify({'message': 'No open order'}), 404


@order_blueprint.route('/add-item', methods=['POST'])
def add_order_item():
    api_key = request.headers.get('Authorization')

    if not api_key:
        return jsonify({'message': 'Not logged in'}), 401

    response = get_user(api_key)

    user = response.get('data')

    if not user:
        return jsonify({'message': 'User not found'}), 404

    book_id = int(request.form['book_id'])
    quantity = int(request.form['quantity'])
    user_id = user['id']

    open_order = Order.query.filter_by(user_id=user_id, is_open=1).first()

    if not open_order:
        open_order = Order()
        open_order.is_open = True
        open_order.user_id = user_id

        order_item = OrderItem(book_id=book_id, quantity=quantity)
        open_order.order_items.append(order_item)
    else:
        found = False

        for item in open_order.order_items:
            if item.book_id == book_id:
                item.quantity += quantity
                found = True

        if not found:
            order_item = OrderItem(book_id=book_id, quantity=quantity)
            open_order.order_items.append(order_item)

    db.session.add(open_order)
    db.session.commit()

    return jsonify({'data': open_order.serialize()}), 200


@order_blueprint.route('/checkout', methods=['POST'])
def checkout():
    api_key = request.headers.get('Authorization')

    if not api_key:
        return jsonify({'message': 'Not logged in'}), 401

    response = get_user(api_key)

    user = response.get('data')

    if not user:
        return jsonify({'message': 'User not found'}), 404

    user_id = user['id']

    open_order = Order.query.filter_by(user_id=user_id, is_open=1).first()

    if open_order:
        open_order.is_open = False

        db.session.add(open_order)
        db.session.commit()

        return jsonify({'data': open_order.serialize()}), 200

    return jsonify({'message': 'No open order'}), 404


@order_blueprint.route('/all', methods=['GET'])
def all_orders():
    orders = Order.query.all()
    orders = [order.serialize() for order in orders]
    return jsonify(orders), 200
