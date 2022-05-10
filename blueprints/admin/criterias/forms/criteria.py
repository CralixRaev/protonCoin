from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired


class CriteriaForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    basis_id = SelectField("Основание", coerce=int, validators=[DataRequired()])
    cost = IntegerField("Цена", validators=[DataRequired()])
    submit = SubmitField('Создать/Изменить')
