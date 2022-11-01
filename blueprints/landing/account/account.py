import os

import flask
from flask import Blueprint, render_template, redirect, url_for, current_app, request
from flask_login import current_user, login_required
from werkzeug.datastructures import MultiDict
from blueprints.landing.account.forms.achievement import AchievementForm
from blueprints.landing.account.forms.main import UserForm
from blueprints.landing.account.forms.password import PasswordForm
from db.models.achievement import AchievementQuery
from db.models.basis import BasisQuery
from db.models.criteria import CriteriaQuery
from db.models.transaction import TransactionQuery
from db.models.user import UserQuery
from uploads import achievement_files

# from util import password_check, save_upload, upload_avatar

account = Blueprint('account', __name__, template_folder='templates', static_folder='static')

@account.route("/", methods=['GET', 'POST'])
@login_required
def index():
    context = {
        'title': "Ваш аккаунт",
        'form_avatar': form_avatar,
        'form_main': form_main,
        'form_password': form_password
    }
    return render_template("account/account_transactions.html", **context)


@account.route("/transactions/", methods=['GET', 'POST'])
@login_required
def transactions():
    form_avatar = AvatarForm()
    context = {
        "title": "Транзакции",
        'form_avatar': form_avatar,
        'withdraws': reversed(TransactionQuery.get_withdraws(current_user.balance)),
        'accruals': reversed(TransactionQuery.get_accruals(current_user.balance))
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
    return render_template("account/account_achievements.html", **context)


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
            return redirect(url_for(".transactions"))
    return render_template("account/account_declare_achievement.html", **context)
