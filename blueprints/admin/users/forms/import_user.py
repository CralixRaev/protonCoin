from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired


class UserImportForm(FlaskForm):
    group_id = SelectField("Класс", coerce=int, validators=[DataRequired(), ])
    file = FileField("Таблица с пользователями",
                     validators=[FileRequired(), FileAllowed(['xlsx'], "Таблица с пользователями")])
    submit = SubmitField('Создать/Изменить')
