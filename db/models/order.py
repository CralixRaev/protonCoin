from db.database import db
from uploads import gift_images


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    gift_id = db.Column(db.Integer, db.ForeignKey("gift.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    is_issued = db.Column(db.Boolean, nullable=False, default=False)
    is_returned = db.Column(db.Boolean, nullable=False, default=False)


class OrderQuery:
    pass

