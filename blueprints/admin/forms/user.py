from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    surname = StringField("Фамилия", validators=[DataRequired()])
    name = StringField("Имя", validators=[DataRequired()])
    patronymic = StringField("Отчество")
    email = EmailField("Электронная почта")
    is_admin = BooleanField("Администратор")
    submit = SubmitField('Создать/Изменить')
