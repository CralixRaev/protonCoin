import flask
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

from db.models.gift import GiftQuery, Gift
from db.models.order import OrderQuery
from db.models.transaction import TransactionQuery
from uploads import gift_images

catalog = Blueprint('catalog', __name__, template_folder='templates', static_folder='static')

ORDER_TYPES = {
    'price_desc': ("Цена ↑ (дорогое наверх)", Gift.price.desc()),
    'price_asc': ("Цена ↓ (дешевое наверх)", Gift.price),
    'name_desc': ("Название ↑", Gift.name.desc()),
    'name_asc': ("Название ↓", Gift.name),
}


@catalog.route("/")
def index():
    order_by_type = request.args.get('order_by', 'price_desc')
    order_by = ORDER_TYPES[order_by_type]
    context = {
        # CHANGEME
        'title': "Подарки",
        'order_by_current': order_by_type,
        'order_by': ORDER_TYPES,
        'gifts': GiftQuery.get_all_gifts(order_by[1]),
    }
    return render_template("catalog/catalog.html", **context)


@catalog.route("/buy")
@login_required
def buy():
    gift = GiftQuery.get_gift_by_id(request.args.get('gift_id'))
    if current_user.balance.amount - gift.price >= 0:
        order = OrderQuery.create_order(gift.id, current_user.id)
        TransactionQuery.create_withdraw(current_user.balance, gift.price,
                                         comment=f"Оплата за заказ №{order.id} ({gift.name})")
        flask.flash(
            f"Заказ на подарок создан, его номер №{order.id}",
            "success")
    else:
        flask.flash("Недостаточно средств", "danger")
    return redirect(url_for(".index"))
