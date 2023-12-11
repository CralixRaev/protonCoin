from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired


class CriteriaForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    basis_id = SelectField("Основание", coerce=int, validators=[DataRequired()])
    cost = IntegerField("Цена", validators=[DataRequired()])
    is_user_achievable = BooleanField(
        "Возможность заявить достижение на данную критерию", validators=[]
    )
    submit = SubmitField("Создать/Изменить")
