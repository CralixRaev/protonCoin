from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired


class UserImportForm(FlaskForm):
    group_id = SelectField(
        "Класс",
        coerce=int,
        validators=[
            DataRequired(),
        ],
    )
    file = FileField(
        "Таблица с пользователями",
        validators=[FileRequired(), FileAllowed(["xlsx"], "Таблица с пользователями")],
    )
    submit = SubmitField("Создать/Изменить")
