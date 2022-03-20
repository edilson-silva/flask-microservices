from os import environ

from dotenv import find_dotenv
from dotenv import load_dotenv
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from routes import blueprint

load_dotenv(find_dotenv())

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['WTF_CSRF_SECRET_KEY'] = environ.get('WTF_CSRF_SECRET_KEY')
app.config['UPLOAD_FOLDER'] = environ.get('static/images')

app.register_blueprint(blueprint)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_message = 'Please, login'
login_manager.login_view = 'frontend.login'

bootstrap = Bootstrap(app)


@login_manager.user_loader
def load_user(user_id):
    return None


if __name__ == '__main__':
    print('\n\n>> Running FRONTEND microservice at 5000 port <<\n\n')
    app.run(debug=True, port=5000)
