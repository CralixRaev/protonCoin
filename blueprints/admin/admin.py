from flask import Blueprint, render_template
from flask_login import login_required

from blueprints.admin.groups.groups import groups
from blueprints.admin.users.users import users
from util import admin_required

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')
admin.register_blueprint(users, url_prefix="/users/")
admin.register_blueprint(groups, url_prefix="/groups/")


@admin.route('/')
@login_required
@admin_required
def index():
    context = {
        'title': 'Главная страница'
    }
    return render_template("admin/index.html", **context)
