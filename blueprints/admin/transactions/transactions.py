import flask
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

from blueprints.admin.transactions.forms.transaction import TransactionForm
from db.models.balances import BalanceQuery
from db.models.transaction import TransactionQuery
from db.models.user import UserQuery
from util import admin_required

transactions = Blueprint('transactions', __name__, template_folder='templates')


@transactions.route("/")
@login_required
@admin_required
def index():
    context = {
        'title': 'Транзакции',
        'transactions': TransactionQuery.get_all_transactions()
    }
    return render_template("transactions/transactions.html", **context)


@transactions.route("/create/", methods=["GET", "POST"])
@login_required
@admin_required
def create():
    balances = BalanceQuery.get_all_balances()
    users_list = [(balance.id, balance) for balance in balances]
    form = TransactionForm()
    form.from_balance_id.choices = users_list
    form.to_balance_id.choices = users_list
    context = {
        'title': "Создать транзакцию",
        'form': form
    }
    if form.validate_on_submit():
        TransactionQuery.create_transaction(form.from_balance_id.data, form.to_balance_id.data,
                                            form.amount.data, form.comment.data)
        flask.flash(f"Транзакция осуществлена.")
        return redirect(url_for('admin.transactions.index'))
    return render_template("transactions/transaction.html", **context)
