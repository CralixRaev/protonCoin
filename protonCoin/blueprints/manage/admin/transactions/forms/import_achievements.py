from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField
from wtforms_components import SelectField
from wtforms.validators import DataRequired


class AchievementImportForm(FlaskForm):
    criteria = SelectField(
        "Критерия",
        coerce=int,
        validators=[
            DataRequired(),
        ],
    )
    file = FileField(
        "Таблица с пользователями (Фамилия, Имя, Отчество, Цифра класса, Буква класса)",
        validators=[FileRequired(), FileAllowed(["xlsx"], "Таблица с пользователями")],
    )
    comment = StringField("Комментарий (к примеру, предмет олимпиады)", validators=[])
    submit = SubmitField("Импортировать")
