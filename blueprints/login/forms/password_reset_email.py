from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PasswordResetForm(FlaskForm):
    email = StringField("Электронная почта", validators=[DataRequired()])
    submit = SubmitField("Восстановить")
