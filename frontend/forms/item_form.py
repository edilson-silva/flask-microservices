from flask_wtf import FlaskForm
from wtforms import HiddenField

from wtforms.validators import DataRequired


class ItemForm(FlaskForm):
    book_id = HiddenField(validators=[DataRequired()])
    quantity = HiddenField(validators=[DataRequired()])
