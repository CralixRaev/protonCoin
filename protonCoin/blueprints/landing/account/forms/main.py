from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms_components import Email


class UserForm(FlaskForm):
    email = EmailField("Электронная почта", validators=[Email()])
    nickname = StringField("Пcевдоним (для игровых серверов)", validators=[])
    submit = SubmitField("Сохранить")
