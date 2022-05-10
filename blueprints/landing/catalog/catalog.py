from flask import Blueprint, render_template

from db.models.gift import GiftQuery
from uploads import gift_images

catalog = Blueprint('catalog', __name__, template_folder='templates', static_folder='static')


@catalog.route("/")
def index():
    context = {
        'title': "Подарки",
        'gifts': GiftQuery.get_all_gifts(),
    }
    return render_template("catalog/catalog.html", **context)
