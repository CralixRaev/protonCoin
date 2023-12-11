from flask import Blueprint, render_template
from flask_login import login_required

from protonCoin.blueprints.manage.admin.achievement.achievement import achievement
from protonCoin.blueprints.manage.admin.basises.basises import basises
from protonCoin.blueprints.manage.admin.criterias.criterias import criterias
from protonCoin.blueprints.manage.admin.gifts.gifts import gifts
from protonCoin.blueprints.manage.admin.groups.groups import groups
from protonCoin.blueprints.manage.admin.news.news import news
from protonCoin.blueprints.manage.admin.orders.orders import orders
from protonCoin.blueprints.manage.admin.transactions.transactions import transactions
from protonCoin.blueprints.manage.admin.users.users import users
from protonCoin.util import admin_required

admin = Blueprint(
    "admin", __name__, template_folder="templates", static_folder="static"
)
admin.register_blueprint(users, url_prefix="/users/")
admin.register_blueprint(groups, url_prefix="/groups/")
admin.register_blueprint(transactions, url_prefix="/transactions/")
admin.register_blueprint(gifts, url_prefix="/gifts/")
admin.register_blueprint(basises, url_prefix="/basises/")
admin.register_blueprint(news, url_prefix="/news/")
admin.register_blueprint(criterias, url_prefix="/criterias/")
admin.register_blueprint(orders, url_prefix="/orders/")
admin.register_blueprint(achievement, url_prefix="/achievement/")


@admin.before_request
@login_required
@admin_required
def before_request():
    pass


@admin.route("/")
def index():
    context = {"title": "Главная страница"}
    return render_template("admin/index.html", **context)
