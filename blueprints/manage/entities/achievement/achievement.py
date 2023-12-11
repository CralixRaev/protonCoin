import flask
from flask import Blueprint, request, current_app

from db.models.achievement import AchievementQuery
from db.models.transaction import TransactionQuery
from util import admin_required, redirect_to_back

achievement_methods = Blueprint("achievement_methods", __name__, static_folder="static")


@achievement_methods.route("/approve/")
def approve():
    achievement_id = int(request.args.get("id"))
    achievement_entity = AchievementQuery.get_achievement_by_id(achievement_id)
    AchievementQuery.approve_achievement(achievement_entity)
    TransactionQuery.create_accrual(
        achievement_entity.user.balance,
        achievement_entity.criteria.cost,
        comment=f"За достижение ({achievement_entity.criteria.basis})"
        f" {achievement_entity.criteria} (ID: {achievement_entity.id})",
    )
    flask.flash(
        f"Достижение одобрено. Ученику {achievement_entity.user.full_name} выдан"
        f" {achievement_entity.criteria.cost} {current_app.config['COIN_UNIT']}",
        "success",
    )
    return redirect_to_back()


@achievement_methods.route("/disapprove/")
def disapprove():
    achievement_id = int(request.args.get("id"))
    reason = request.args.get("reason")
    achievement_entity = AchievementQuery.get_achievement_by_id(achievement_id)
    AchievementQuery.disapprove_achievement(achievement_entity, reason)
    flask.flash("Достижение отклонено", "danger")
    return redirect_to_back()


@achievement_methods.route("/disapprove_existing/")
@admin_required
def disapprove_existing():
    achievement_id = int(request.args.get("id"))
    reason = request.args.get("reason")
    achievement_entity = AchievementQuery.get_achievement_by_id(achievement_id)
    AchievementQuery.disapprove_existing_achievement(
        achievement_entity,
        f"Отмена подтверждения достижения " f"администратором: {reason}",
    )
    TransactionQuery.create_withdraw(
        achievement_entity.user.balance,
        achievement_entity.criteria.cost,
        comment=f"За отмену подтверждения достижения администратором"
        f" ({achievement_entity.criteria.basis})"
        f" {achievement_entity.criteria} (ID: {achievement_entity.id})",
    )

    flask.flash(
        f"Начисление отменено, достижение отклонено, создана новая транзакция,"
        f" со счёта {achievement_entity.user.full_name} списаны"
        f" {achievement_entity.criteria.cost} {current_app.config['COIN_UNIT']}",
        "danger",
    )
    return redirect_to_back()
