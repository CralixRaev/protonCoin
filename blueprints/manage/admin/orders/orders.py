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

orders = Blueprint('orders', __name__, template_folder='templates')


@orders.route('/')
@login_required
@admin_required
def index():
    context = {
        'title': 'Заказы',
        'awaiting_orders': OrderQuery.get_awaited_orders()
    }
    return render_template("orders/orders.html", **context)


@orders.route('/issue/')
@login_required
@admin_required
def issue():
    order_id = int(request.args.get('id'))
    order = OrderQuery.get_order_by_id(order_id)
    OrderQuery.issue_order(order)
    flask.flash(f"Заказ успешно выдан", "success")
    return redirect(url_for('admin.orders.index'))


@orders.route('/return/')
@login_required
@admin_required
def order_return():
    order_id = int(request.args.get('id'))
    order = OrderQuery.get_order_by_id(order_id)
    TransactionQuery.create_accrual(order.user.balance, order.gift.price,
                                    comment=f"Отмена заказа №{order.id}")
    OrderQuery.return_order(order)
    flask.flash(f"Заказ отменён,"
                f" {order.gift.price}"
                f" {current_app.config['COIN_UNIT']} возвращены на счет покупателя", "success")
    return redirect(url_for('admin.orders.index'))
