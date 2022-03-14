from os import environ

from dotenv import find_dotenv
from dotenv import load_dotenv
from flask import Flask
from flask.sessions import SecureCookieSessionInterface
from flask_login import LoginManager
from flask_migrate import Migrate

import models
from routes import user_blueprint

load_dotenv(find_dotenv())

app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS').lower() in ("true", "1")

models.init_app(app)
app.register_blueprint(user_blueprint)

login_manager = LoginManager(app)
migrate = Migrate(app, models.db)


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.filter_by(id=user_id).first()


@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic', '', 1)
        user = models.User.query.filter_by(api_key=api_key).first()

        if user:
            return user

    return None


class CustomSessionInterface(SecureCookieSessionInterface):
    """
    Prevent creating session from API requests
    """

    def save_session(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        return super(CustomSessionInterface, self)


if __name__ == '__main__':
    print('\n\n>> Running USER microservice at 5001 port <<\n\n')
    app.run(debug=True, port=5001)
