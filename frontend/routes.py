from flask import Blueprint
from flask import render_template
from flask import session
from flask_login import current_user

from api.book_client import BookClient
from api.order_client import OrderClient

blueprint = Blueprint('frontend', __name__)


@blueprint.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        session['order'] = OrderClient.get_order_from_session()

    try:
        books = BookClient.get_books()
    except:
        books = {'data': []}

    return render_template('index.html', books=books)
