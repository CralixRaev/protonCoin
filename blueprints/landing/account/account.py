import os

import flask
from flask import Blueprint, render_template, redirect, url_for, current_app, request
from flask_login import current_user, login_required
from rcon import Client
from werkzeug.datastructures import MultiDict
from blueprints.landing.account.forms.achievement import AchievementForm
from blueprints.landing.account.forms.avatar import AvatarForm
from blueprints.landing.account.forms.main import UserForm
from blueprints.landing.account.forms.password import PasswordForm
from db.models.achievement import AchievementQuery
from db.models.basis import BasisQuery
from db.models.criteria import CriteriaQuery
from db.models.order import OrderQuery
from db.models.transaction import TransactionQuery
from db.models.user import UserQuery
from uploads import avatars, achievement_files

from util import password_check, save_upload, upload_avatar

account = Blueprint('account', __name__, template_folder='templates', static_folder='static')


def _avatar_form_handler(form: AvatarForm):
    if current_user.avatar and current_user.avatar != 'default.png':
        try:
            os.remove(avatars.path(current_user.avatar))
        except FileNotFoundError:
            current_app.logger.warning("Could not remove avatar!")
    UserQuery.update_avatar(current_user, upload_avatar(form.image.data))
    flask.flash("Аватар успешно обновлен", "success")
    return redirect(url_for(request.endpoint))


def _check_password(old: str, new: str, confirm: str) -> str | None:
    if not current_user.check_password(old):
        return "Неправильный старый пароль"
    if new != confirm:
        return "Пароли не совпадают"
    if not password_check(new)['password_ok']:
        return "Пароль не соответствует требованиям безопасности. Нужна одна цифра и одна заглавная буква. Не ругайтесь, все на ваше же благо)"
    return None


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
        _avatar_form_handler(form_avatar)
    elif form_password.validate_on_submit():
        error = _check_password(form_password.old_password.data,
                                form_password.password.data, form_password.confirm.data)
        if error:
            flask.flash(error, "danger")
        else:
            UserQuery.update_password(current_user, form_password.password.data)
            flask.flash("Пароль успешно обновлен", "success")
        return redirect(url_for(".index"))
    elif form_main.validate_on_submit():
        UserQuery.update_email(current_user, form_main.email.data)
        nickname = form_main.nickname.data
        if nickname != current_user.nickname:
            UserQuery.set_nickname(current_user, nickname)
            with Client(current_app.config['RCON_IP'],
                        int(current_app.config['RCON_PORT']),
                        passwd=current_app.config['RCON_PASSWORD']) as client:
                response = client.run('whitelist', 'add', nickname)
                print('rcon', response)
        flask.flash("Данные успешно обновлены", "success")
        return redirect(url_for(".index"))
    context['form_main'] = UserForm(MultiDict(current_user.__dict__.items()))
    return render_template("account/account_info.html", **context)


@account.route("/transactions/", methods=['GET', 'POST'])
@login_required
def transactions():
    form_avatar = AvatarForm()
    context = {
        "title": "Транзакции",
        'form_avatar': form_avatar,
        'withdraws': TransactionQuery.get_withdraws(current_user.balance),
        'accruals': TransactionQuery.get_accruals(current_user.balance)
    }
    if form_avatar.validate_on_submit():
        _avatar_form_handler(form_avatar)
    return render_template("account/account_transactions.html", **context)


@account.route("/achievements/", methods=['GET', 'POST'])
@login_required
def achievements():
    form_avatar = AvatarForm()
    context = {
        "title": "Достижения",
        'form_avatar': form_avatar,
        'achievements': AchievementQuery.get_achievements_by_user(current_user)
    }
    if form_avatar.validate_on_submit():
        _avatar_form_handler(form_avatar)
    return render_template("account/account_achievements.html", **context)\

@account.route("/orders/", methods=['GET', 'POST'])
@login_required
def orders():
    form_avatar = AvatarForm()
    context = {
        "title": "Достижения",
        'form_avatar': form_avatar,
        'orders': OrderQuery.order_by_user(current_user.id)
    }
    if form_avatar.validate_on_submit():
        _avatar_form_handler(form_avatar)
    return render_template("account/account_orders.html", **context)

@account.route("/cancel_order/<int:order_id>")
@login_required
def cancel_order(order_id: int):
    order = OrderQuery.get_order_by_id(order_id)
    if order.user_id != current_user.id or not order.cancellation_available:
        flask.abort(400)
    OrderQuery.cancel_order_user(order)
    return redirect(url_for(".orders"))


@account.route("/declare_achievement/", methods=["GET", "POST"])
@login_required
def declare_achievement():
    form_avatar = AvatarForm()
    form = AchievementForm()
    basises = BasisQuery.get_all_basises()
    form.criteria_id.choices = [
        (basis.name, [(criteria.id, criteria) for criteria in basis.criteria]) for basis in basises]
    context = {
        "title": "Заявить о достижении",
        'form_avatar': form_avatar,
        "form": form
    }
    if form_avatar.validate_on_submit():
        _avatar_form_handler(form_avatar)
    if form.validate_on_submit():
        if not CriteriaQuery.get_criteria_by_id(form.criteria_id.data).is_user_achievable:
            flask.flash("Упс... Это начислят автоматически - без твоего участия! ✨🔮", "warning")
        else:
            achievement_file = None
            if form.file.data:
                achievement_file = save_upload(form.file.data, achievement_files)
            AchievementQuery.create_achievement(form.criteria_id.data, current_user.id,
                                                achievement_file if form.file.data else None,
                                                form.comment.data)
            flask.flash("Достижение принято. Жди одобрения классным руководителем ⌛", "success")
        if form.do_not_redirect.data == "True":
            return redirect(url_for(".declare_achievement"))
        else:
            return redirect(url_for(".transactions"))
    return render_template("account/account_declare_achievement.html", **context)

