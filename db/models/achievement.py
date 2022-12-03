import types
from datetime import datetime
from enum import Enum

from flask_login import current_user
from flask_restful import fields
from sqlalchemy import or_, and_, alias
from sqlalchemy.orm import backref, aliased
from sqlalchemy.sql import functions, expression

from db.database import db
from db.models.basis import Basis
from db.models.criteria import Criteria
from db.models.group import Group
from db.models.user import User
from uploads import achievement_files


class AchievementStatusEnum(Enum):
    awaiting_approval = "awaiting_approval"
    approved = "approved"
    disapproved = "disapproved"


STATUS_TO_STRING = {
    AchievementStatusEnum.awaiting_approval: 'Ожидает обработки',
    AchievementStatusEnum.approved: 'Одобрено',
    AchievementStatusEnum.disapproved: 'Отклонено'
}


class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    criteria_id = db.Column(db.Integer, db.ForeignKey("criteria.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    achievement_file = db.Column(db.String(1024), nullable=True)
    comment = db.Column(db.String(4096), nullable=True)
    creation_date = db.Column(db.DateTime, default=datetime.now)
    edit_date = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    status = db.Column(db.Enum(AchievementStatusEnum),
                       default=AchievementStatusEnum.awaiting_approval, nullable=False)
    disapproval_reason = db.Column(db.String(4096), nullable=True, default=None)
    approved_disapproved_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True,
                                        default=None)

    user = db.relation("User", foreign_keys=[user_id], backref=backref('achievements', order_by=id))
    approved_disapproved_user = db.relation("User", foreign_keys=[approved_disapproved_by])
    criteria = db.relation("Criteria", back_populates='achievements')

    @property
    def achievement_file_path(self) -> str | None:
        if self.achievement_file:
            return achievement_files.url(self.achievement_file)
        return None

    @property
    def status_translation(self) -> str:
        return STATUS_TO_STRING[self.status]

    @staticmethod
    def __json__():
        _json = {
            'id': fields.Integer(),
            'user': fields.Nested(User.__json__()),
            'approved_disapproved_user': fields.Nested(User.__json__()),
            'criteria': fields.Nested(Criteria.__json__()),
            'achievement_file_path': fields.String(),
            'comment': fields.String(),
            'status': fields.FormattedString("{status.value}"),
            'status_translation': fields.String(),
            'disapproval_reason': fields.String()
        }
        return _json


class AchievementQuery:
    @staticmethod
    def create_achievement(criteria_id: int, user_id: int, achievement_file: str,
                           comment: str) -> Achievement:
        db.session.rollback()

        achievement = Achievement()
        achievement.criteria_id = criteria_id
        achievement.user_id = user_id
        achievement.achievement_file = achievement_file
        achievement.comment = comment

        db.session.add(achievement)
        db.session.commit()

        return achievement

    @staticmethod
    def total_count(is_teacher: bool = False) -> int:
        if is_teacher:
            user_alias = aliased(User)
            return Achievement.query.join(user_alias, user_alias.id == Achievement.user_id).filter(user_alias.group_id == current_user.group_id).count()
        else:
            return Achievement.query.count()

    @staticmethod
    def get_api(start: int = 0, length: int = 10, search: str | None = None, order_expr=None,
                status=None, is_teacher=False) -> (
            int, list[Achievement]):
        achievement_query = Achievement.query
        user_alias, approved_by_user_alias = aliased(User), aliased(User)
        user_group_alias = aliased(Group)
        criteria_alias, basis_alias = aliased(Criteria), aliased(Basis)
        achievement_query = achievement_query.join(user_alias, user_alias.id == Achievement.user_id)
        achievement_query = achievement_query.join(user_group_alias, user_group_alias.id == user_alias.group_id)
        achievement_query = achievement_query.join(approved_by_user_alias,
                                                   approved_by_user_alias.id == Achievement.approved_disapproved_by,
                                                   isouter=True)  # we need outer here because some achievements have approved_by user = none
        achievement_query = achievement_query.join(criteria_alias,
                                                   criteria_alias.id == Achievement.criteria_id)
        achievement_query = achievement_query.join(basis_alias,
                                                   basis_alias.id == criteria_alias.basis_id)
        if is_teacher:
            achievement_query = achievement_query.filter(user_group_alias.id == current_user.group_id)
        if status:
            achievement_query = achievement_query.filter(Achievement.status == status)
        count = achievement_query.count()
        if search:
            user_full_name = user_alias.surname + ' ' + user_alias.name + ' ' + user_alias.patronymic
            achievement_query = achievement_query.filter(or_(user_full_name.ilike(f'%{search}%'),
                                                             criteria_alias.name.ilike(
                                                                 f'%{search}%'),
                                                             basis_alias.name.ilike(
                                                                 f'%{search}%'),
                                                             Achievement.comment.ilike(
                                                                 f'%{search}%')))
            count = achievement_query.count()
        if order_expr is not None:
            achievement_query = achievement_query.order_by(*order_expr)
        achievement_query = achievement_query.limit(length).offset(start)
        return count, achievement_query.all()

    @staticmethod
    def get_achievements(group: Group = None) -> tuple[int, list[Achievement]]:
        achievements_query = Achievement.query.filter(Achievement.is_approved == False,
                                                      Achievement.is_disapproved == False)
        if group:
            users = db.session.query(User.id).filter(User.group_id == group.id).all()
            achievements_query = achievements_query.filter(
                Achievement.user_id.in_([id for id, in users]))
        return achievements_query.count(), achievements_query.order_by(Achievement.id.desc()).all()

    @staticmethod
    def get_achievements_approved_disapproved() -> list[Achievement]:
        return Achievement.query.filter(or_(and_(Achievement.is_approved == True,
                                                 Achievement.is_disapproved == False),
                                            and_(Achievement.is_approved == False,
                                                 Achievement.is_disapproved == True)
                                            )).order_by(Achievement.id.desc()).all()

    @staticmethod
    def get_achievement_by_id(achievement_id) -> Achievement:
        return Achievement.query.get(achievement_id)

    @staticmethod
    def get_achievements_by_user(user: User) -> Achievement:
        return Achievement.query.filter(Achievement.user_id == user.id).order_by(
            Achievement.id.desc()).all()

    @staticmethod
    def approve_achievement(achievement: Achievement):
        achievement.approved_disapproved_by = current_user.id
        achievement.status = AchievementStatusEnum.approved
        db.session.commit()

    @staticmethod
    def disapprove_achievement(achievement: Achievement, reason: str):
        achievement.approved_disapproved_by = current_user.id
        achievement.status = AchievementStatusEnum.disapproved
        achievement.disapproval_reason = reason
        db.session.commit()

    @staticmethod
    def disapprove_existing_achievement(achievement: Achievement, reason: str):
        achievement.approved_disapproved_by = current_user.id
        achievement.status = AchievementStatusEnum.disapproved
        achievement.disapproval_reason = reason
        db.session.commit()
