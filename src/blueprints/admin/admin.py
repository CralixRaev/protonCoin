from flask import Blueprint, render_template
from flask_login import login_required

from src.blueprints.admin.groups.groups import groups
from src.blueprints.admin.transactions.transactions import transactions
from src.blueprints.admin.users.users import users
from src.util import admin_required

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')
admin.register_blueprint(users, url_prefix="/users/")
admin.register_blueprint(groups, url_prefix="/groups/")
admin.register_blueprint(transactions, url_prefix="/transactions/")


@admin.route('/')
@login_required
@admin_required
def index():
    context = {
        'title': 'Главная страница'
    }
    return render_template("admin/index.html", **context)
