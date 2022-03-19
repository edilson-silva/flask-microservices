import requests

from . import BOOK_API_URL


class BookClient:

    @staticmethod
    def get_books():
        url = f'{BOOK_API_URL}all'
        response = requests.get(url)
        return response.json()

    @staticmethod
    def get_book(slug):
        url = f'{BOOK_API_URL}{slug}'
        response = requests.get(url)
        return response.json()
