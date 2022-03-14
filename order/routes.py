from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Order(db.Table):

    id = db.Column(db.String)
    books = db.Column()
