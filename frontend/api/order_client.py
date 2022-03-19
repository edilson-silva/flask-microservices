import requests
from flask import session

from . import ORDER_API_URL


class OrderClient:

    @staticmethod
    def get_order():
        headers = {
            'Authorization': session.get('user_api_key')
        }

        response = requests.get(ORDER_API_URL, headers=headers)
        return response.json()

    @staticmethod
    def add_to_cart(book_id, quantity=1):
        headers = {
            'Authorization': session.get('user_api_key')
        }

        payload = {
            'book_id': book_id,
            'quantity': quantity
        }

        url = f'{ORDER_API_URL}add-item'
        response = requests.post(url, data=payload, headers=headers)
        return response.json()

    @staticmethod
    def checkout():
        headers = {
            'Authorization': session.get('user_api_key')
        }

        url = f'{ORDER_API_URL}checkout'
        response = requests.get(url, headers=headers)
        return response.json()

    @staticmethod
    def get_order_from_session():
        default_order = {
            'items': {}
        }

        return session.get('order', default_order)
