import flask
from flask import Blueprint, render_template, current_app, url_for, redirect, request
from flask_login import login_required, current_user

from db.models.achievement import AchievementQuery
from db.models.transaction import TransactionQuery
from util import teacher_or_admin_required, admin_required

achievement = Blueprint('achievement', __name__, template_folder='templates')


@achievement.route('/')
def index():
    context = {
        'title': f'Достижения',
        'achievements_none': AchievementQuery.get_achievements_none(group if group else None),
        'achievements_approved_disapproved': AchievementQuery.get_achievements_approved_disapproved()
    }
    return render_template("achievement/achievements.html", **context)


@achievement.route('/approve/')
@login_required
@teacher_or_admin_required
def approve():
    achievement_id = int(request.args.get('id'))
    achievement_entity = AchievementQuery.get_achievement_by_id(achievement_id)
    AchievementQuery.approve_achievement(achievement_entity)
    TransactionQuery.create_accrual(achievement_entity.user.balance,
                                    achievement_entity.criteria.cost,
                                    comment=f"За достижение ({achievement_entity.criteria.basis})"
                                            f" {achievement_entity.criteria} (ID: {achievement_entity.id})")
    flask.flash(f"Достижение одобрено. Ученику {achievement_entity.user.full_name} выдан"
                f" {achievement_entity.criteria.cost} {current_app.config['COIN_UNIT']}", "success")
    return redirect(url_for('admin.achievements.index'))


@achievement.route('/disapprove/')
@login_required
@teacher_or_admin_required
def disapprove():
    achievement_id = int(request.args.get('id'))
    reason = request.args.get('reason')
    achievement_entity = AchievementQuery.get_achievement_by_id(achievement_id)
    AchievementQuery.disapprove_achievement(achievement_entity, reason)
    flask.flash(f"Достижение отклонено", "danger")
    return redirect(url_for('admin.achievements.index'))


@achievement.route('/disapprove_existing/')
@login_required
@admin_required
def disapprove_existing():
    achievement_id = int(request.args.get('id'))
    reason = request.args.get('reason')
    achievement_entity = AchievementQuery.get_achievement_by_id(achievement_id)
    AchievementQuery.disapprove_existing_achievement(achievement_entity,
                                                     f"Отмена подтверждения достижения "
                                                     f"администратором: {reason}")
    TransactionQuery.create_withdraw(achievement_entity.user.balance,
                                     achievement_entity.criteria.cost,
                                     comment=f"За отмену подтверждения достижения администратором"
                                             f" ({achievement_entity.criteria.basis})"
                                             f" {achievement_entity.criteria} (ID: {achievement_entity.id})")

    flask.flash(
        f"Начисление отменено, достижение отклонено, создана новая транзакция,"
        f" со счёта {achievement_entity.user.full_name} списаны"
        f" {achievement_entity.criteria.cost} {current_app.config['COIN_UNIT']}",
        "danger")
    return redirect(url_for('admin.achievements.index'))
