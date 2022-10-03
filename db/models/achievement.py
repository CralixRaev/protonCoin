from datetime import datetime

from sqlalchemy import or_, and_
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
    is_approved = db.Column(db.Boolean, default=False, nullable=False)
    is_disapproved = db.Column(db.Boolean, default=False, nullable=False)

    user = db.relation("User", back_populates='achievements')
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
    def approve_achievement(achievement: Achievement):
        achievement.is_approved = True
        db.session.commit()

    @staticmethod
    def disapprove_achievement(achievement: Achievement):
        achievement.is_disapproved = True
        db.session.commit()
