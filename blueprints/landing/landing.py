from flask import Blueprint, render_template

from blueprints.landing.account.account import account
from blueprints.landing.catalog.catalog import catalog

landing = Blueprint('landing', __name__, template_folder='templates', static_folder='static')
landing.register_blueprint(catalog, url_prefix="/catalog")
landing.register_blueprint(account, url_prefix="/account")

@landing.route("/")
def index():
    return render_template("landing/base.html")

