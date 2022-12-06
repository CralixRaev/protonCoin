import os.path

import flask
from flask import Blueprint, render_template, redirect, request, url_for, Request, Response, \
    current_app
from flask_login import login_required
from werkzeug.datastructures import MultiDict

from db.models.order import OrderQuery
from db.models.transaction import TransactionQuery
from uploads import gift_images
from util import admin_required

orders = Blueprint('orders', __name__, template_folder='templates', static_folder='static')


@orders.route('/')
@login_required
@admin_required
def index():
    context = {
        'title': 'Заказы',
    }
    return render_template("orders/orders.html", **context)


@orders.route('/deliver/<int:order_id>')
@login_required
@admin_required
def deliver(order_id: int):
    order = OrderQuery.get_order_by_id(order_id)
    OrderQuery.deliver_order(order)
    flask.flash(f"Заказ успешно выдан", "success")
    return redirect(url_for('manage.admin.orders.index'))


@orders.route('/cancel/<int:order_id>')
@login_required
@admin_required
def order_cancel(order_id):
    order = OrderQuery.get_order_by_id(order_id)
    OrderQuery.cancel_order(order)
    flask.flash(f"Заказ отменён,"
                f" {order.gift.price}"
                f" {current_app.config['COIN_UNIT']} возвращены на счет покупателя", "success")
    return redirect(url_for('manage.admin.orders.index'))
