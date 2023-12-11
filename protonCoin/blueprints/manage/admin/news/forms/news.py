from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired()])
    description = TextAreaField("Описание", validators=[DataRequired()])
    submit = SubmitField("Создать/Изменить")
