from flask import Blueprint

from protonCoin.blueprints.manage.admin.admin import admin
from protonCoin.blueprints.manage.entities.methods import methods
from protonCoin.blueprints.manage.teacher.teacher import teacher

manage = Blueprint(
    "manage", __name__, template_folder="templates", static_folder="static"
)
manage.register_blueprint(admin, url_prefix="/admin")
manage.register_blueprint(teacher, url_prefix="/teacher")
manage.register_blueprint(methods, url_prefix="/methods")
