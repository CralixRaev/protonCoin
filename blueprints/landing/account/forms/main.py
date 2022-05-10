from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField, \
    TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email

from uploads import avatars


class UserForm(FlaskForm):
    email = EmailField("Электронная почта")
    submit = SubmitField('Сохранить')
