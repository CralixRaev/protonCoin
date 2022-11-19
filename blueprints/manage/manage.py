from flask import Blueprint

from blueprints.manage.admin.admin import admin
from blueprints.manage.teacher.teacher import teacher

manage = Blueprint('manage', __name__, template_folder='templates', static_folder='static')
manage.register_blueprint(admin, url_prefix="/admin")
manage.register_blueprint(teacher, url_prefix="/teacher")
