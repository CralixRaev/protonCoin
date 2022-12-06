from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField, \
    TextAreaField, IntegerField
from wtforms.validators import DataRequired, InputRequired

from uploads import gift_images


class GiftForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    description = TextAreaField("Описание", validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired()])
    stock = IntegerField('Остаток', validators=[InputRequired()])
    image = FileField('Изображение', validators=[
        FileAllowed(gift_images, 'Картинка')
    ])
    submit = SubmitField('Создать/Изменить')
