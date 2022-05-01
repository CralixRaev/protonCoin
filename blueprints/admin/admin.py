import flask
from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import login_required

from blueprints.admin.forms.user import UserForm
from db.models.user import UserQuery
from util import admin_required

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


@admin.route('/')
@login_required
@admin_required
def index():
    context = {
        'title': 'Главная страница'
    }
    return render_template("admin/index.html", **context)


# TODO: make users different blueprint

@admin.route('/users/')
@login_required
@admin_required
def users():
    context = {
        'title': 'Пользователи',
        'users': UserQuery.get_all_users()
    }
    return render_template("admin/users.html", **context)


@admin.route('/create_user/', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    form = UserForm()
    context = {
        'title': 'Создать пользователя',
        'form': form
    }
    if form.validate_on_submit():
        user, password = UserQuery.create_user(form.name.data, form.surname.data, form.patronymic.data, form.email.data)
        flask.flash(f"Пользователь успешно создан. Его логин: {user.login}, пароль: {password}")
        return redirect(url_for('admin.users'))
    return render_template("admin/user.html", **context)


@admin.route('/new_password/', methods=['GET', 'POST'])
@login_required
@admin_required
def new_password():
    password = UserQuery.new_password(request.args.get('id'))
    flask.flash(f"Новый пароль для пользователя: {password}")
    return redirect(url_for('admin.users'))

