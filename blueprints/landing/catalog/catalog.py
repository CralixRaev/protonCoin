import flask
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

from db.models.gift import GiftQuery
from db.models.order import OrderQuery
from db.models.transaction import TransactionQuery
from uploads import gift_images

catalog = Blueprint('catalog', __name__, template_folder='templates', static_folder='static')


@catalog.route("/")
def index():
    context = {
        'title': "Подарки",
        'gifts': GiftQuery.get_all_gifts(),
    }
    return render_template("catalog/catalog.html", **context)


@catalog.route("/buy")
@login_required
def buy():
    gift = GiftQuery.get_gift_by_id(request.args.get('gift_id'))
    # TODO: gifts receiving
    if current_user.balance.amount - gift.price >= 0:
        TransactionQuery.create_withdraw(current_user.balance, gift.price,
                                         comment=f"Оплата за подарок {gift.name}")
        order = OrderQuery.create_order(gift.id, current_user.id)
        flask.flash(f"Заказ на подарок создан, его номер {order.id}. Обратитесь к ... для получения")
    else:
        flask.flash("Недостаточно средств")
    return redirect(url_for(".index"))
