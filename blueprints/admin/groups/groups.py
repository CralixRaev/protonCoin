import flask
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

from blueprints.admin.forms.group import GroupForm
from db.models.group import GroupQuery
from util import admin_required

groups = Blueprint('groups', __name__, template_folder='templates')


@groups.route("/")
@login_required
@admin_required
def index():
    context = {
        'title': 'Классы',
        'groups': GroupQuery.get_all_groups()
    }
    return render_template("groups/groups.html", **context)


@groups.route("/create_group/", methods=['GET', 'POST'])
@login_required
@admin_required
def create_group():
    form = GroupForm()
    context = {
        'title': 'Создать класс',
        'form': form
    }
    if form.validate_on_submit():
        GroupQuery.create_group(form.stage.data, form.letter.data)
        flask.flash(f"Класс успешно создан.")
        return redirect(url_for('admin.groups.index'))
    return render_template("groups/group.html", **context)
