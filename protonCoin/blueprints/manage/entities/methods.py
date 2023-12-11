from flask import Blueprint
from flask_login import login_required

from protonCoin.blueprints.manage.entities.achievement.achievement import (
    achievement_methods,
)
from protonCoin.blueprints.manage.entities.user.user import user_methods
from protonCoin.util import teacher_or_admin_required

methods = Blueprint("methods", __name__)


@methods.before_request
@login_required
@teacher_or_admin_required
def before_request():
    pass


methods.register_blueprint(user_methods, url_prefix="/user")
methods.register_blueprint(achievement_methods, url_prefix="/achievement")
