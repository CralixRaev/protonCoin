from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired
from wtforms_components import SelectField

from uploads import achievement_files


class AchievementForm(FlaskForm):
    criteria_id = SelectField("Критерий *", coerce=int, validators=[DataRequired()])
    comment = TextAreaField("Комментарий")
    file = FileField(
        "Файл, подтверждающий достижение *",
        validators=[
            FileAllowed(achievement_files, "Картинка или документ"),
            FileRequired(),
        ],
    )
    do_not_redirect = HiddenField(
        "Не перенаправлять на index, а дать отправить ещё одно достижение",
        default="False",
    )
    submit_button = SubmitField("Отправить")
