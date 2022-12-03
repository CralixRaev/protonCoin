from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    surname = StringField("Фамилия", validators=[DataRequired()])
    name = StringField("Имя", validators=[DataRequired()])
    patronymic = StringField("Отчество")
    group_id = SelectField("Класс", coerce=int)
    email = EmailField("Электронная почта")
    is_admin = BooleanField("Администратор")
    is_teacher = BooleanField("Учитель")
    submit = SubmitField('Создать/Изменить')
