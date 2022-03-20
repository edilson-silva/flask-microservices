from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_login import current_user

from api.book_client import BookClient
from api.order_client import OrderClient
from api.user_client import UserClient
from forms.login_form import LoginForm

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


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            api_key = UserClient.login(form)
            if api_key:
                session['user_api_key'] = api_key
                user = UserClient.get_user()
                session['user'] = user['result']

                order = OrderClient.get_order()
                if order.get('result'):
                    session['order'] = order['result']

                flash('Welcome back')
                return redirect(url_for('frontend.index'))
            else:
                flash('Cannot Login')
        else:
            flash('Cannot Login')

    return render_template('login.html', form=form)
