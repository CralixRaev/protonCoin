from functools import wraps

import flask
from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import login_required, current_user

from db.models.user import UserQuery

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:
            return flask.abort(403)
        return func(*args, **kwargs)

    return decorated_view


@admin.route('/')
@login_required
@admin_required
def index():
    context = {
        'title': 'Главная страница'
    }
    return render_template("admin/index.html", **context)


@admin.route('/users/')
@login_required
@admin_required
def users():
    context = {
        'title': 'Пользователи',
        'users': UserQuery.get_all_users()
    }
    return render_template("admin/users.html", **context)
