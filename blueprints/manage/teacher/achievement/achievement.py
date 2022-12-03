import flask
from flask import Blueprint, render_template, current_app, url_for, redirect, request
from flask_login import login_required, current_user
from flask_restful import marshal

from db.models.achievement import AchievementQuery
from db.models.transaction import TransactionQuery
from util import teacher_or_admin_required, admin_required

achievement = Blueprint('achievement', __name__, template_folder='templates', static_folder='static')


@achievement.route('/')
def index():
    context = {
        'title': f'Достижения',
    }
    return render_template("achievement_teacher/list_achievement.html", **context)
