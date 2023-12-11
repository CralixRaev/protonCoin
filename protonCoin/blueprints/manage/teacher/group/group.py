import flask
from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user

from protonCoin.db.models.user import UserQuery
from protonCoin.util import teacher_required

group = Blueprint(
    "group", __name__, template_folder="templates", static_folder="static"
)


@group.route("/")
@login_required
@teacher_required
def index():
    context = {
        "title": f'Ваш {current_user.group.name if current_user.group else "класс"}',
        "users": current_user.group.users if current_user.group else [],
    }
    return render_template("group/group.html", **context)


@group.route("/new_password/", methods=["GET", "POST"])
@login_required
@teacher_required
def new_password():
    password = UserQuery.new_password(request.args.get("id"))
    flask.flash(f"Новый пароль для пользователя: {password}")
    return redirect(url_for("teacher.index"))
