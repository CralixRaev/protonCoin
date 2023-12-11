import flask
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

from protonCoin.blueprints.manage.admin.basises.forms.basis import BasisForm
from protonCoin.db.models.basis import BasisQuery
from protonCoin.util import admin_required

basises = Blueprint(
    "basises", __name__, template_folder="templates", static_folder="static"
)


@basises.route("/")
@login_required
@admin_required
def index():
    context = {"title": "Основания", "basises": BasisQuery.get_all_basises()}
    return render_template("basises/basises.html", **context)


@basises.route("/create_basis/", methods=["GET", "POST"])
@login_required
@admin_required
def create_basis():
    form = BasisForm()
    context = {"title": "Создать основание", "form": form}
    if form.validate_on_submit():
        BasisQuery.create_basis(form.name.data)
        flask.flash("Основание успешно создано.", "success")
        return redirect(url_for("manage.admin.basises.index"))
    return render_template("basises/basis.html", **context)
