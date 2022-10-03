import io

import flask
import openpyxl
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from openpyxl.workbook import Workbook

from blueprints.admin.transactions.forms.import_achievements import AchievementImportForm
from blueprints.admin.transactions.forms.transaction import TransactionForm
from db.models.balances import BalanceQuery
from db.models.basis import BasisQuery
from db.models.criteria import CriteriaQuery
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
    users_list = [(balance.id, balance) for balance in
                  sorted(balances, key=lambda x: x.user.full_name if x.user else "0")]
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


@transactions.route('/import/', methods=['GET', 'POST'])
@login_required
@admin_required
def import_achievements():
    form = AchievementImportForm()
    basises = BasisQuery.get_all_basises()
    form.criteria.choices = [(basis.name, [(criteria.id, criteria) for criteria in basis.criteria]) for basis in basises]
    context = {
        'title': 'Импортировать достижения',
        'form': form
    }
    if form.validate_on_submit():
        criteria = CriteriaQuery.get_criteria_by_id(form.criteria.data)
        not_found_users = []
        table = form.file.data
        table = io.BytesIO(table.stream.read())
        wb_read = openpyxl.load_workbook(table)
        ws_read = wb_read.active
        for i, cells in enumerate(ws_read.iter_rows(2), start=2):
            surname, name, patronymic, number, letter = cells
            user = UserQuery.find_user(surname.value, name.value,
                                       patronymic.value, number.value, letter.value)
            if user:
                TransactionQuery.create_accrual(user.balance, criteria.cost, f"За критерий ({criteria.basis.name}) {criteria.name} (начислено автоматически)")
            else:
                not_found_users.append((surname.value, name.value, patronymic.value))
        not_found_users = ',\n'.join([' '.join(i) for i in not_found_users])
        flask.flash(f"Начисления успешно созданы.\nНе найденные пользователи: {not_found_users}")
        return redirect(url_for(".index"))
    return render_template("transactions/import.html", **context)
