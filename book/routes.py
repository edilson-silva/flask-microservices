from flask import Blueprint

book_blueprint = Blueprint('book_api_routes', __name__, url_prefix='/api/book')


@book_blueprint.route('/all', methods=['GET'])
def get_all_books():
    return 'All books'


@book_blueprint.route('/create', methods=['POST'])
def create_book():
    return 'Book created'


@book_blueprint.route('/<slug>', methods=['GET'])
def book_details(slug):
    return f'Book details {slug}'
