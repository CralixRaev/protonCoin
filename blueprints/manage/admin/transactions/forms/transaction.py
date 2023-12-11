from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired


class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass


class TransactionForm(FlaskForm):
    from_balance_id = NonValidatingSelectField("От", validators=[DataRequired()])
    to_balance_id = NonValidatingSelectField("К", validators=[DataRequired()])
    amount = IntegerField("Количество", validators=[DataRequired()])
    comment = StringField("Комментарий")
    submit = SubmitField("Создать")
