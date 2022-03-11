import models

from flask import Flask
from routes import user_blueprint

app = Flask(__name__)
app.register_blueprint(user_blueprint)


if __name__ == '__main__':
    app.run(debug=True)
