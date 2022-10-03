from flask import Blueprint, render_template
from flask_login import login_required

from blueprints.admin.achievements.achievements import achievements
from blueprints.admin.basises.basises import basises
from blueprints.admin.criterias.criterias import criterias
from blueprints.admin.gifts.gifts import gifts
from blueprints.admin.groups.groups import groups
from blueprints.admin.orders.orders import orders
from blueprints.admin.transactions.transactions import transactions
from blueprints.admin.users.users import users
from util import admin_required

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')
admin.register_blueprint(users, url_prefix="/users/")
admin.register_blueprint(groups, url_prefix="/groups/")
admin.register_blueprint(transactions, url_prefix="/transactions/")
admin.register_blueprint(gifts, url_prefix="/gifts/")
admin.register_blueprint(basises, url_prefix="/basises/")
admin.register_blueprint(criterias, url_prefix="/criterias/")
admin.register_blueprint(orders, url_prefix="/orders/")
admin.register_blueprint(achievements, url_prefix="/achievements/")


@admin.route('/')
@login_required
@admin_required
def index():
    context = {
        'title': 'Главная страница'
    }
    return render_template("admin/index.html", **context)
