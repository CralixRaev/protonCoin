import flask
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from werkzeug.datastructures import MultiDict

from blueprints.manage.admin.groups.forms.group import GroupForm
from db.models.group import GroupQuery
from util import admin_required

groups = Blueprint(
    "groups", __name__, template_folder="templates", static_folder="static"
)


@groups.route("/")
@login_required
@admin_required
def index():
    context = {
        "title": "Классы",
    }
    return render_template("groups/groups.html", **context)


@groups.route("/create_group/", methods=["GET", "POST"])
@login_required
@admin_required
def create_group():
    form = GroupForm()
    context = {"title": "Создать класс", "form": form}
    if form.validate_on_submit():
        GroupQuery.create_group(form.stage.data, form.letter.data)
        flask.flash("Класс успешно создан.", "success")
        return redirect(url_for("manage.admin.groups.index"))
    return render_template("groups/group.html", **context)


@groups.route("/edit/", methods=["GET", "POST"])
@login_required
@admin_required
def edit_user():
    user = GroupQuery.get_group_by_id(request.args.get("id"))
    form = GroupForm()
    context = {"title": "Редактировать класс", "form": form}
    if form.validate_on_submit():
        GroupQuery.update_group(user, form.stage.data, form.letter.data)
        flask.flash("Класс успешно обновлен.", "success")
        return redirect(url_for("manage.admin.groups.index"))
    model_data = MultiDict(user.__dict__.items())
    form = GroupForm(model_data)
    context["form"] = form
    return render_template("groups/group.html", **context)


@groups.route("/delete/")
@login_required
@admin_required
def delete_group():
    group_id = request.args.get("id")
    group = GroupQuery.get_group_by_id(group_id)
    GroupQuery.delete_group(group)
    flask.flash(f"Класс ID: {group.id} - {group.name} успешно удалён", "success")
    return redirect(url_for("manage.admin.groups.index"))
