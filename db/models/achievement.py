import types
from datetime import datetime
from enum import Enum

from flask_login import current_user
from flask_restful import fields
from sqlalchemy import or_, and_
from sqlalchemy.orm import backref
from sqlalchemy.sql import functions, expression

from db.database import db
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
            'criteria': fields.Nested(Criteria.__json__()),
            'achievement_file_path': fields.String(),
            'comment': fields.String(),
            'status': fields.FormattedString("{status.value}"),
            'status_translation': fields.String(),
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
    def total_count() -> int:
        return Achievement.query.count()

    @staticmethod
    def get_api(start: int = 0, length: int = 10, search: str | None = None, order_expr=None, status=None) -> (
            int, list[Achievement]):
        achievement_query = Achievement.query
        if status:
            achievement_query = achievement_query.filter(Achievement.status == status)
        count = achievement_query.count()
        if search:
            count = achievement_query.count()
        print(order_expr)
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
        achievement.is_approved = True
        db.session.commit()

    @staticmethod
    def disapprove_achievement(achievement: Achievement, reason: str):
        achievement.approved_disapproved_by = current_user.id
        achievement.is_disapproved = True
        achievement.disapproval_reason = reason
        db.session.commit()

    @staticmethod
    def disapprove_existing_achievement(achievement: Achievement, reason: str):
        achievement.approved_disapproved_by = current_user.id
        achievement.is_disapproved = True
        achievement.is_approved = False
        achievement.disapproval_reason = reason
        db.session.commit()
