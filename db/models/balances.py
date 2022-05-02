from db.database import db


class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True, index=True)
    amount = db.Column(db.Integer, nullable=False, default=0)

    user = db.relationship('User', back_populates='balance', uselist=False)


class BalanceQuery:
    pass