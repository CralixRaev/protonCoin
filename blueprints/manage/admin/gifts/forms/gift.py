from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, InputRequired

from uploads import gift_images


class NullableIntegerField(IntegerField):
    """
    An IntegerField where the field can be null if the input data is an empty
    string.
    """

    def process_formdata(self, valuelist):
        if valuelist:
            if valuelist[0] == "":
                self.data = None
            else:
                try:
                    if valuelist[0] is not None:
                        self.data = int(valuelist[0])
                except ValueError:
                    self.data = None
                    raise ValueError(self.gettext("Not a valid integer value"))


class GiftForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    description = TextAreaField("Описание", validators=[DataRequired()])
    price = IntegerField("Цена до акции", validators=[DataRequired()])
    promo_price = NullableIntegerField(
        "Цена до скидки (если указать, эта цена на сайте будет зачеркнутой)"
    )
    stock = IntegerField("Остаток", validators=[InputRequired()])
    image = FileField("Изображение", validators=[FileAllowed(gift_images, "Картинка")])
    submit = SubmitField("Создать/Изменить")
