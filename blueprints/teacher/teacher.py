from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

from blueprints.teacher.achievements.achievements import achievements
from blueprints.teacher.group.group import group
from util import admin_required, teacher_required

teacher = Blueprint('teacher', __name__, template_folder='templates', static_folder='static')
teacher.register_blueprint(group, url_prefix="/group/")
teacher.register_blueprint(achievements, url_prefix="/achievements/")


@teacher.route('/')
@login_required
@teacher_required
def index():
    return redirect(url_for('teacher.group.index'))
