import flask
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from werkzeug.datastructures import MultiDict

from protonCoin.blueprints.manage.admin.criterias.forms.criteria import CriteriaForm
from protonCoin.db.models.basis import BasisQuery
from protonCoin.db.models.criteria import CriteriaQuery
from protonCoin.util import admin_required

criterias = Blueprint(
    "criterias", __name__, template_folder="templates", static_folder="static"
)


@criterias.route("/")
@login_required
@admin_required
def index():
    context = {
        "title": "Критерии",
    }
    return render_template("criterias/criterias.html", **context)


@criterias.route("/create_criteria/", methods=["GET", "POST"])
@login_required
@admin_required
def create_criteria():
    basises = BasisQuery.get_all_basises()
    form = CriteriaForm()
    form.basis_id.choices = [(basis.id, basis.name) for basis in basises]
    context = {"title": "Создать критерий", "form": form}
    if form.validate_on_submit():
        CriteriaQuery.create_criteria(
            form.name.data, form.basis_id.data, form.cost.data
        )
        flask.flash("Критерий успешно создан.", "success")
        return redirect(url_for("manage.admin.criterias.index"))
    return render_template("criterias/criteria.html", **context)


@criterias.route("/edit/", methods=["GET", "POST"])
@login_required
@admin_required
def edit_criteria():
    basises = BasisQuery.get_all_basises()
    criteria = CriteriaQuery.get_criteria_by_id(request.args.get("id"))
    form = CriteriaForm()
    form.basis_id.choices = [(basis.id, basis.name) for basis in basises]
    context = {"title": "Редактировать критерию", "form": form}
    if form.validate_on_submit():
        CriteriaQuery.update_criteria(
            criteria,
            form.name.data,
            form.basis_id.data,
            form.cost.data,
            form.is_user_achievable.data,
        )
        flask.flash("Критерия успешно обновлена", "success")
        return redirect(url_for(".index"))
    context["form"] = CriteriaForm(MultiDict(criteria.__dict__.items()))
    context["form"].basis_id.choices = [(basis.id, basis.name) for basis in basises]
    return render_template("criterias/criteria.html", **context)


@criterias.route("/delete/")
@login_required
@admin_required
def delete_criteria():
    criteria_id = request.args.get("id")
    criteria = CriteriaQuery.get_criteria_by_id(criteria_id)
    flask.flash(
        f"Критерия ID: {criteria.id} - ({criteria.basis.name}) {criteria.name} успешно удалёна",
        "success",
    )
    CriteriaQuery.delete_criteria(criteria)
    return redirect(url_for(".index"))
