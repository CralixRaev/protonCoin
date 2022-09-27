from flask import Blueprint, render_template

from blueprints.landing.account.account import account
from blueprints.landing.catalog.catalog import catalog
from db.models.balances import BalanceQuery

landing = Blueprint('landing', __name__, template_folder='templates', static_folder='static')
landing.register_blueprint(catalog, url_prefix="/catalog")
landing.register_blueprint(account, url_prefix="/account")


@landing.route("/")
def index():
    context = {
        'title': "Главная страница",
        'top_balances': enumerate(BalanceQuery.top_balances(10), start=1),
        'colors': ["#AF9500", '#B4B4B4', "#6A3805"]
    }
    return render_template("landing/top.html", **context)
