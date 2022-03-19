import requests
from flask import session

from . import USER_API_URL


class UserClient:

    @staticmethod
    def login(form):
        api_key = None
        payload = {
            'username': form.username.data,
            'password': form.password.data
        }

        url = f'{USER_API_URL}login'
        response = requests.post(url, data=payload)

        if response:
            api_key = response.json().get('api_key')

        return api_key

    @staticmethod
    def get_user():
        headers = {
            'Authorization': session.get('user_api_key')
        }

        response = requests.get(USER_API_URL, headers=headers)
        user = response.json()
        return user

    @staticmethod
    def create_user(form):
        user = None
        payload = {
            'username': form.username.data,
            'password': form.password.data
        }

        url = f'{USER_API_URL}create'
        response = requests.post(url, data=payload)

        if response:
            user = response.json()

        return user

    @staticmethod
    def user_exists(username):
        url = f'{USER_API_URL}{username}/exists'
        response = requests.get(url)
        return response.ok
