from datetime import datetime

from flask_login import current_user
from sqlalchemy import or_, and_
from sqlalchemy.orm import backref

from db.database import db
from db.models.user import User
from uploads import achievement_files


class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    criteria_id = db.Column(db.Integer, db.ForeignKey("criteria.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    achievement_file = db.Column(db.String(1024), nullable=True)
    comment = db.Column(db.String(4096), nullable=True)
    creation_date = db.Column(db.DateTime, default=datetime.now)
    edit_date = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    is_approved = db.Column(db.Boolean, default=False, nullable=False)
    is_disapproved = db.Column(db.Boolean, default=False, nullable=False)
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
    def status(self) -> str:
        if self.is_approved:
            return "Одобрено"
        elif self.is_disapproved:
            return "Отклонено"
        else:
            return "Ожидает обработки"

    @property
    def status_color_class(self) -> str:
        if self.is_approved:
            return "text-success fw-bold"
        elif self.is_disapproved:
            return "text-danger"
        else:
            return ""


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
    def get_achievements_by_group(group) -> list[Achievement]:
        users = db.session.query(User.id).filter(User.group_id == group.id).all()
        return Achievement.query.filter(Achievement.user_id.in_([id for id, in users]),
                                        Achievement.is_approved == False,
                                        Achievement.is_disapproved == False).all()

    @staticmethod
    def get_achievements_none() -> list[Achievement]:
        return Achievement.query.filter(Achievement.is_approved == False,
                                        Achievement.is_disapproved == False) \
            .order_by(Achievement.id.desc()).all()

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

