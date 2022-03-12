from os import environ

from dotenv import find_dotenv
from dotenv import load_dotenv
from flask import Flask

from routes import book_blueprint

load_dotenv(find_dotenv())

app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS').lower() in ("true", "1")

app.register_blueprint(book_blueprint)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
