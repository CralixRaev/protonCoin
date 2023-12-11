from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired


class PasswordForm(FlaskForm):
    old_password = PasswordField("Старый пароль", [DataRequired()])
    password = PasswordField("Новый пароль", [DataRequired()])
    confirm = PasswordField("Повторите пароль", [DataRequired()])
    submit = SubmitField("Сохранить")
