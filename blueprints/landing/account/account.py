import os

import flask
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from werkzeug.datastructures import MultiDict
from werkzeug.utils import secure_filename

from blueprints.landing.account.forms import achievement
from blueprints.landing.account.forms.achievement import AchievementForm
from blueprints.landing.account.forms.avatar import AvatarForm
from blueprints.landing.account.forms.main import UserForm
from blueprints.landing.account.forms.password import PasswordForm
from db.models.achievement import AchievementQuery
from db.models.basis import BasisQuery
from db.models.criteria import CriteriaQuery
from db.models.transaction import TransactionQuery
from db.models.user import UserQuery
from uploads import avatars, achievement_files
from transliterate import translit

from util import password_check

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
        if not password_check(form_password.password.data)['password_ok']:
            flask.flash("Пароль не соответствует требованиям безопасности")
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


@account.route("/transactions/")
@login_required
def transactions():
    context = {
        "title": "Транзакции",
        'withdraws': reversed(TransactionQuery.get_withdraws(current_user.balance)),
        'accruals': reversed(TransactionQuery.get_accruals(current_user.balance))
    }
    return render_template("account/transactions.html", **context)


@account.route("/declare_achievement/", methods=["GET", "POST"])
@login_required
def declare_achievement():
    form = AchievementForm()
    basises = BasisQuery.get_all_basises()
    form.criteria_id.choices = [(basis.name, [(criteria.id, criteria) for criteria in basis.criteria]) for basis in basises]
    context = {
        "title": "Заявить достижение",
        "form": form
    }
    if form.validate_on_submit():
        achievement_file = None
        if form.file.data:
            form.file.data.filename = secure_filename(translit(form.file.data.filename, 'ru', True))
            achievement_file = achievement_files.save(form.file.data)
        AchievementQuery.create_achievement(form.criteria_id.data, current_user.id,
                                            achievement_file if form.file.data else None,
                                            form.comment.data)
        flask.flash("Достижение принято. Ожидайте одобрения классным руководителем")
        # criteria = CriteriaQuery.get_criteria_by_id(form.criteria_id.data)
        # TransactionQuery.create_accrual(current_user.balance, criteria.cost,
        # f"За критерий {criteria.name} - {criteria.basis.name}")
        return redirect(url_for(".transactions"))
    return render_template("account/declare_achievement.html", **context)