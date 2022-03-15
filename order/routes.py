from os import environ

from flask import Blueprint
from flask import jsonify

from models import Order

order_blueprint = Blueprint('order_api_routes', __name__, url_prefix='/api/order')

USER_API = environ.get('USER_API')


@order_blueprint.route('/all', methods=['GET'])
def all_orders():
    orders = Order.query.all()
    orders = [order.serialize() for order in orders]
    return jsonify(orders), 200
