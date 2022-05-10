import os

import flask
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from werkzeug.datastructures import MultiDict

from blueprints.landing.account.forms.avatar import AvatarForm
from blueprints.landing.account.forms.main import UserForm
from blueprints.landing.account.forms.password import PasswordForm
from db.models.user import UserQuery
from uploads import avatars

account = Blueprint('account', __name__, template_folder='templates', static_folder='static')


@account.route("/", methods=['GET', 'POST'])
@login_required
def index():
    form_avatar = AvatarForm()
    form_main = UserForm()
    form_password = PasswordForm()
    context = {
        'title': "Ваш аккаунт",
        'form_avatar': form_avatar,
        'form_main': form_main,
        'form_password': form_password
    }
    if form_avatar.validate_on_submit():
        image = form_avatar.image.data
        if current_user.avatar and current_user.avatar != 'default.png':
            os.remove(avatars.path(current_user.avatar))
        filename = avatars.save(image)
        UserQuery.update_avatar(current_user, filename)
        flask.flash("Аватар успешно обновлен")
        return redirect(url_for(".index"))
    elif form_password.validate_on_submit():
        if not current_user.check_password(form_password.old_password.data):
            flask.flash("Неправильный старый пароль")
            return redirect(url_for(".index"))
        if form_password.password.data != form_password.confirm.data:
            flask.flash("Пароли не совпадают")
            return redirect(url_for(".index"))
        UserQuery.update_password(current_user, form_password.password.data)
        flask.flash("Пароль успешно обновлен")
        return redirect(url_for(".index"))
    elif form_main.validate_on_submit():
        UserQuery.update_email(current_user, form_main.email.data)
        flask.flash("Почта успешно обновлена")
        return redirect(url_for(".index"))
    context['form_main'] = UserForm(MultiDict(current_user.__dict__.items()))
    return render_template("account/account.html", **context)
