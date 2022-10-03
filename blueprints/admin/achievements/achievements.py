import flask
from flask import Blueprint, render_template, redirect, request, url_for, Request, Response, \
    current_app
from flask_login import login_required, current_user
from werkzeug.datastructures import MultiDict

from db.models.achievement import AchievementQuery
from db.models.order import OrderQuery
from db.models.transaction import TransactionQuery
from db.models.user import UserQuery
from uploads import gift_images
from util import admin_required, teacher_required

achievements = Blueprint('achievements', __name__, template_folder='templates')


@achievements.route('/')
@login_required
@teacher_required
def index():
    context = {
        'title': f'Достижения',
        'achievements_none': AchievementQuery.get_achievements_none(),
        'achievements_approved_disapproved': AchievementQuery.get_achievements_approved_disapproved()
    }
    return render_template("achievements/achievements.html", **context)


@achievements.route('/approve/')
@login_required
@teacher_required
def approve():
    achievement_id = int(request.args.get('id'))
    achievement = AchievementQuery.get_achievement_by_id(achievement_id)
    AchievementQuery.approve_achievement(achievement)
    TransactionQuery.create_accrual(achievement.user.balance, achievement.criteria.cost,
                                    comment=f"За достижение ({achievement.criteria.basis})"
                                            f" {achievement.criteria} (ID: {achievement.id})")
    flask.flash(f"Достижение одобрено. Ученику {achievement.user.full_name} выдан"
                f" {achievement.criteria.cost} {current_app.config['COIN_UNIT']}")
    return redirect(url_for('teacher.achievements.index'))


@achievements.route('/disapprove/')
@login_required
@teacher_required
def disapprove():
    achievement_id = int(request.args.get('id'))
    achievement = AchievementQuery.get_achievement_by_id(achievement_id)
    AchievementQuery.disapprove_achievement(achievement)
    flask.flash(f"Достижение отклонено")
    return redirect(url_for('teacher.achievements.index'))