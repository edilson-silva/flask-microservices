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
from forms.register_form import RegistrationForm

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


@blueprint.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data

            if UserClient.user_exists(username):
                flash("Please try another user name")
                return render_template('register.html', form=form)
            else:
                user = UserClient.create_user(form)
                if user:
                    flash("Registered. Please login.")
                    return redirect(url_for('frontend.index'))
        else:
            flash("Errors")

    return render_template('register.html', form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            api_key = UserClient.login(form)
            if api_key:
                session['user_api_key'] = api_key
                user = UserClient.get_user()
                session['user'] = user['data']

                order = OrderClient.get_order()
                if order.get('data'):
                    session['order'] = order['data']

                flash('Welcome back')
                return redirect(url_for('frontend.index'))
            else:
                flash('Cannot Login')
        else:
            flash('Cannot Login')

    return render_template('login.html', form=form)


@blueprint.route('/logout', methods=['GET'])
def logout():
    session.clear()
    flash('Logged out')
    return redirect(url_for('frontend.index'))
