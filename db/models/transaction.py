from datetime import datetime

from db.database import db


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    from_balance_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    to_balance_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255), nullable=True)
    creation_date = db.Column(db.DateTime, default=datetime.now)

    from_balance = db.relation("Balance", "balance.id")
    to_balance = db.relation("Balance", "balance.id")
