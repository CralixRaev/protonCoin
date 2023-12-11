import flask
from flask import request, Blueprint

from protonCoin.db.models.user import UserQuery
from protonCoin.util import admin_required, redirect_to_back

user_methods = Blueprint("user_methods", __name__)


@user_methods.route("/delete/")
@admin_required
def delete_user():
    user_id = request.args.get("id")
    user = UserQuery.get_user_by_id(user_id)
    UserQuery.delete_user(user)
    flask.flash(
        f"Пользователь ID: {user.id} - {user.full_name} успешно удалён", "success"
    )
    return redirect_to_back()


@user_methods.route("/new_password/", methods=["GET", "POST"])
def new_password():
    password = UserQuery.new_password(request.args.get("id"))
    flask.flash(f"Новый пароль для пользователя: {password}", "success")
    return redirect_to_back()
