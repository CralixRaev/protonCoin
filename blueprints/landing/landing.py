from flask import Blueprint, render_template

from blueprints.landing.account.account import account
from blueprints.landing.catalog.catalog import catalog
from db.models.balances import BalanceQuery
from db.models.transaction import TransactionQuery

landing = Blueprint('landing', __name__, template_folder='templates', static_folder='static',
                    static_url_path='/static/landing/')
landing.register_blueprint(catalog, url_prefix="/catalog")
landing.register_blueprint(account, url_prefix="/account")


@landing.route("/")
def index():
    context = {
        'title': "Главная страница",
        'top_balances': enumerate(BalanceQuery.top_balances(10), start=1),
        'last_accruals': TransactionQuery.last_accruals
    }
    return render_template("landing/top.html", **context)
