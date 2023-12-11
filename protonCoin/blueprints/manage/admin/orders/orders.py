import flask
from flask import Blueprint, render_template, redirect, url_for, current_app
from flask_login import login_required

from protonCoin.db.models.order import OrderQuery
from protonCoin.util import admin_required

orders = Blueprint(
    "orders", __name__, template_folder="templates", static_folder="static"
)


@orders.route("/")
@login_required
@admin_required
def index():
    context = {
        "title": "Заказы",
    }
    return render_template("orders/orders.html", **context)


@orders.route("/deliver/<int:order_id>")
@login_required
@admin_required
def deliver(order_id: int):
    order = OrderQuery.get_order_by_id(order_id)
    OrderQuery.deliver_order(order)
    flask.flash("Заказ успешно выдан", "success")
    return redirect(url_for("manage.admin.orders.index"))


@orders.route("/cancel/<int:order_id>")
@login_required
@admin_required
def order_cancel(order_id):
    order = OrderQuery.get_order_by_id(order_id)
    OrderQuery.cancel_order(order)
    flask.flash(
        f"Заказ отменён,"
        f" {order.gift.price}"
        f" {current_app.config['COIN_UNIT']} возвращены на счет покупателя",
        "success",
    )
    return redirect(url_for("manage.admin.orders.index"))
