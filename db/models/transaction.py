from datetime import datetime

import flask

from db.database import db
from db.models.balances import BalanceQuery


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    from_balance_id = db.Column(db.Integer, db.ForeignKey("balance.id"), nullable=False)
    to_balance_id = db.Column(db.Integer, db.ForeignKey("balance.id"), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255), nullable=True)
    creation_date = db.Column(db.DateTime, default=datetime.now)

    from_balance = db.relation("Balance", foreign_keys=[from_balance_id])
    to_balance = db.relation("Balance", foreign_keys=[to_balance_id])


class TransactionQuery:
    @staticmethod
    def get_all_transactions() -> list[Transaction]:
        return Transaction.query.all()

    @staticmethod
    def create_transaction(from_balance_id, to_balance_id, amount, comment=None) -> Transaction:
        try:
            transaction = Transaction()
            transaction.from_balance_id = from_balance_id
            transaction.to_balance_id = to_balance_id
            transaction.amount = amount
            transaction.comment = comment
            db.session.add(transaction)
            print(from_balance_id)
            from_balance = BalanceQuery.get_balance_by_id(from_balance_id)
            to_balance = BalanceQuery.get_balance_by_id(to_balance_id)
            print(from_balance)
            if not from_balance.is_bank:
                transaction.from_balance.amount -= amount

            if not to_balance.is_bank:
                transaction.to_balance.amount += amount
            db.session.commit()
            return transaction
        except Exception as e:
            db.session.rollback()
            flask.current_app.logger.error("Error while creating transaction", e)
            flask.abort(500)

    @staticmethod
    def get_withdraws(balance) -> list[Transaction]:
        return Transaction.query.filter(Transaction.from_balance_id == balance.id).all()

    @staticmethod
    def get_accruals(balance) -> list[Transaction]:
        return Transaction.query.filter(Transaction.to_balance_id == balance.id).all()

    @staticmethod
    def create_accrual(balance, amount, comment=None) -> Transaction:
        # user with id 1 will be bank. always. TRUST ME
        return TransactionQuery.create_transaction(1, balance.id, amount, comment=comment)

    @staticmethod
    def create_withdraw(balance, amount, comment=None) -> Transaction:
        return TransactionQuery.create_transaction(balance.id, 1, amount, comment=comment)

