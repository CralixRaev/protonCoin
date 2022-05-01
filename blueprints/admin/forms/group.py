from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class GroupForm(FlaskForm):
    stage = IntegerField("Цифра", validators=[DataRequired()])
    letter = StringField("Буква", validators=[DataRequired()])
    submit = SubmitField('Создать/Изменить')
