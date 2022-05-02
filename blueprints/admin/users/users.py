import flask
from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required
from werkzeug.datastructures import MultiDict

from blueprints.admin.users.forms.user import UserForm
from db.models.group import GroupQuery
from db.models.user import UserQuery
from util import admin_required

users = Blueprint('users', __name__, template_folder='templates')


@users.route('/')
@login_required
@admin_required
def index():
    context = {
        'title': 'Пользователи',
        'users': UserQuery.get_all_users()
    }
    return render_template("users/users.html", **context)


@users.route('/create/', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    groups = GroupQuery.get_all_groups()
    group_list = [(-1, "Нет")] + [(group.id, group.name) for group in groups]
    form = UserForm()
    form.group_id.choices = group_list
    context = {
        'title': 'Создать пользователя',
        'form': form
    }
    if form.validate_on_submit():
        user, password = UserQuery.create_user(form.name.data, form.surname.data,
                                               form.patronymic.data, form.email.data,
                                               form.is_admin.data,
                                               form.group_id.data if form.group_id.data != -1 else None)
        flask.flash(f"Пользователь успешно создан. Его логин: {user.login}, пароль: {password}")
        return redirect(url_for('admin.users.index'))
    return render_template("users/user.html", **context)


@users.route('/edit/', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user():
    user = UserQuery.get_user_by_id(request.args.get('id'))
    groups = GroupQuery.get_all_groups()
    group_list = [(-1, "Нет")] + [(group.id, group.name) for group in groups]
    form = UserForm()
    form.group_id.choices = group_list
    context = {
        'title': 'Редактировать пользователя',
        'form': form
    }
    if form.validate_on_submit():
        UserQuery.update_user(user, form.name.data, form.surname.data,
                              form.patronymic.data, form.email.data, form.is_admin.data,
                              form.group_id.data if form.group_id.data != -1 else None)
        print(form.group_id.data)
        flask.flash(f"Пользователь успешно обновлен.")
        return redirect(url_for('admin.users.index'))
    model_data = MultiDict(user.__dict__.items())
    model_data['group_id'] = -1 if not model_data['group_id'] else model_data['group_id']
    form = UserForm(model_data)
    form.group_id.choices = group_list
    context['form'] = form
    return render_template("users/user.html", **context)


@users.route('/new_password/', methods=['GET', 'POST'])
@login_required
@admin_required
def new_password():
    password = UserQuery.new_password(request.args.get('id'))
    flask.flash(f"Новый пароль для пользователя: {password}")
    return redirect(url_for('admin.users.index'))
