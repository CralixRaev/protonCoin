from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class BasisForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    submit = SubmitField("Создать/Изменить")
