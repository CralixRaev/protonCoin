from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired


class TransactionForm(FlaskForm):
    from_balance_id = SelectField("От", coerce=int, validators=[DataRequired()])
    to_balance_id = SelectField("К", coerce=int, validators=[DataRequired()])
    amount = IntegerField("Количество", validators=[DataRequired()])
    comment = StringField("Комментарий")
    submit = SubmitField("Создать")
