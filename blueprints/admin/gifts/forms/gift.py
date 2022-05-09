from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField, \
    TextAreaField, IntegerField
from wtforms.validators import DataRequired


class GiftForm(FlaskForm):
    name = StringField("Фамилия", validators=[DataRequired()])
    description = TextAreaField("Имя", validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired()])
    image = FileField('Изображение', validators=[
        FileRequired(),
        FileAllowed(['png'], 'Картинка в формате PNG')
    ])
    submit = SubmitField('Создать/Изменить')
