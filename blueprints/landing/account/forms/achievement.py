from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField,\
    TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email
from wtforms_components import SelectField

from uploads import avatars


class AchievementForm(FlaskForm):
    criteria_id = SelectField("Критерий", coerce=int)
    file = FileField("Файл, подтверждающий достижение")
    submit = SubmitField('Отправить')
