from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField, \
    TextAreaField, IntegerField
from wtforms.validators import DataRequired
from wtforms_components import Email

from uploads import avatars


class UserForm(FlaskForm):
    email = EmailField("Электронная почта", validators=[Email()])
    nickname = StringField("Пcевдоним (для игровых серверов)", validators=[])
    submit = SubmitField('Сохранить')
