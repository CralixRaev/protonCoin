import flask
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

from blueprints.admin.basises.forms.basis import BasisForm
from blueprints.admin.criterias.forms.criteria import CriteriaForm
from db.models.basis import BasisQuery
from db.models.criteria import CriteriaQuery
from util import admin_required

criterias = Blueprint('criterias', __name__, template_folder='templates')


@criterias.route("/")
@login_required
@admin_required
def index():
    context = {
        'title': 'Критерии',
        'criterias': CriteriaQuery.get_all_criterias()
    }
    return render_template("criterias/criterias.html", **context)


@criterias.route("/create_criteria/", methods=['GET', 'POST'])
@login_required
@admin_required
def create_criteria():
    basises = BasisQuery.get_all_basises()
    form = CriteriaForm()
    form.basis_id.choices = [(basis.id, basis.name) for basis in basises]
    context = {
        'title': 'Создать критерий',
        'form': form
    }
    if form.validate_on_submit():
        CriteriaQuery.create_criteria(form.name.data, form.basis_id.data, form.cost.data)
        flask.flash(f"Критерий успешно создан.")
        return redirect(url_for('admin.criterias.index'))
    return render_template("criterias/criteria.html", **context)
