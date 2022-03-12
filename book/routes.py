from flask import Blueprint
from flask import jsonify
from flask import request
from flask import make_response

from models import Book
from models import db

book_blueprint = Blueprint('book_api_routes', __name__, url_prefix='/api/book')


@book_blueprint.route('/all', methods=['GET'])
def get_all_books():
    all_books = Book.query.all()
    books = [book.serialize() for book in all_books]

    response = {'message': 'Returning all book', 'data': books}
    return jsonify(response)


@book_blueprint.route('/create', methods=['POST'])
def create_book():
    try:
        book = Book()
        book.name = request.form['name']
        book.slug = request.form['slug']
        book.price = request.form['price']
        book.image = request.form['image']

        db.session.add(book)
        db.session.commit()

        response = {'message': 'Book created', 'data': book.serialize()}
    except Exception as e:
        print(f'Create book error: {e}')
        response = {'message': 'Book create error'}

    return jsonify(response)


@book_blueprint.route('/<slug>', methods=['GET'])
def book_details(slug):
    book = Book.query.filter_by(slug=slug).first()

    if book:
        response = {'data': book.serialize()}
        return make_response(jsonify(response), 200)
    else:
        response = {'message': 'Book not found'}
        return make_response(jsonify(response), 404)
