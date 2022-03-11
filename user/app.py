import models

from flask import Flask
from routes import user_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'QBzTq9qaCXwbxV0StBehew'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database/user.db'

models.init_app(app)
app.register_blueprint(user_blueprint)


if __name__ == '__main__':
    app.run(debug=True)
