from datetime import datetime

from db.database import db
from uploads import gift_images


class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    criteria_id = db.Column(db.Integer, db.ForeignKey("criteria.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    achievement_file = db.Column(db.String(1024), nullable=True)
    comment = db.Column(db.String(4096), nullable=True)
    creation_date = db.Column(db.DateTime, default=datetime.now)
    is_approved = db.Column(db.Boolean, default=False, nullable=False)
    is_disapproved = db.Column(db.Boolean, default=False, nullable=False)


class AchievementQuery:
    pass
