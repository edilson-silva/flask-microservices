from os import environ

from flask import Blueprint

order_blueprint = Blueprint('order_api_routes', __name__, '/api/order')

USER_API = environ.get('USER_API')

print('USE', USER_API)
