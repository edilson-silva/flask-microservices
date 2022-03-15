from os import environ

import requests
from flask import Blueprint
from flask import jsonify

from models import Order

order_blueprint = Blueprint('order_api_routes', __name__, url_prefix='/api/order')

USER_API = environ.get('USER_API')


def get_user(api_key):
    headers = {
        'Authorization': api_key
    }

    response = requests.get(USER_API, headers=headers)

    if not response.ok:
        return {'message': 'User nor authorized'}

    user = response.json()
    return user


@order_blueprint.route('/all', methods=['GET'])
def all_orders():
    orders = Order.query.all()
    orders = [order.serialize() for order in orders]
    return jsonify(orders), 200
