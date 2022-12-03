from flask import Blueprint, redirect, url_for
from flask_login import login_required

from blueprints.manage.teacher.achievement.achievement import achievement
from blueprints.manage.teacher.group.group import group
from util import teacher_required

teacher = Blueprint('teacher', __name__, template_folder='templates', static_folder='static')
teacher.register_blueprint(group, url_prefix="/group/")
teacher.register_blueprint(achievement, url_prefix="/achievement/")


@teacher.before_request
@login_required
@teacher_required
def before_request():
    pass


@teacher.route('/')
@login_required
@teacher_required
def index():
    return redirect(url_for('manage.teacher.group.index'))
