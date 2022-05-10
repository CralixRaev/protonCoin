from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField, \
    TextAreaField, IntegerField
from wtforms.validators import DataRequired

from uploads import avatars


class AvatarForm(FlaskForm):
    image = FileField('Новый аватар', validators=[
        FileRequired(),
        FileAllowed(avatars, 'Картинка')
    ])