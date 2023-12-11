from datetime import datetime

import flask
from flask_restful import fields
from sqlalchemy import or_
from sqlalchemy.orm import aliased

from db.database import db
from db.models.balances import BalanceQuery, Balance
from db.models.user import User


class Transaction(db.Model):
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True
    )
    from_balance_id = db.Column(db.Integer, db.ForeignKey("balance.id"), nullable=False)
    to_balance_id = db.Column(db.Integer, db.ForeignKey("balance.id"), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255), nullable=True)
    creation_date = db.Column(db.DateTime, default=datetime.now)

    from_balance = db.relation("Balance", foreign_keys=[from_balance_id])
    to_balance = db.relation("Balance", foreign_keys=[to_balance_id])

    @staticmethod
    def __json__() -> dict:
        _json = {
            "id": fields.Integer(),
            "from_balance": fields.Nested(Balance.__json__()),
            "to_balance": fields.Nested(Balance.__json__()),
            "from_user": fields.Nested(User.__json__(), attribute="from_balance.user"),
            "to_user": fields.Nested(User.__json__(), attribute="to_balance.user"),
            "amount": fields.Integer(),
            "comment": fields.String(),
            "creation_date": fields.DateTime(dt_format="iso8601"),
        }
        return _json


class TransactionQuery:
    @staticmethod
    def get_all_transactions() -> list[Transaction]:
        return Transaction.query.order_by(Transaction.id.desc()).all()

    @staticmethod
    def get_api(
        start: int = 0, length: int = 10, search: str | None = None, order_expr=None
    ) -> (int, list[Transaction]):
        # this is probably the hardest query what i ever wrote
        transaction_query = Transaction.query
        from_balance_alias = aliased(Balance)
        to_balance_alias = aliased(Balance)
        from_user_alias = aliased(User)
        to_user_alias = aliased(User)
        transaction_query = transaction_query.join(
            from_balance_alias, Transaction.from_balance
        )
        transaction_query = transaction_query.join(
            to_balance_alias, Transaction.to_balance
        )
        transaction_query = transaction_query.join(
            from_user_alias,
            from_user_alias.id == from_balance_alias.user_id,
            isouter=True,
        )
        transaction_query = transaction_query.join(
            to_user_alias, to_user_alias.id == to_balance_alias.user_id, isouter=True
        )
        count = transaction_query.count()
        if search:
            from_name = (
                from_user_alias.surname
                + " "
                + from_user_alias.name
                + " "
                + from_user_alias.patronymic
            )
            to_name = (
                to_user_alias.surname
                + " "
                + to_user_alias.name
                + " "
                + to_user_alias.patronymic
            )
            transaction_query = transaction_query.filter(
                or_(
                    from_name.ilike(f"%{search}%"),
                    to_name.ilike(f"%{search}%"),
                    Transaction.comment.ilike(f"%{search}%"),
                )
            )
            count = transaction_query.count()
        if order_expr is not None:
            transaction_query = transaction_query.order_by(*order_expr)
        transaction_query = transaction_query.limit(length).offset(start)
        return count, transaction_query.all()

    @staticmethod
    def create_transaction(
        from_balance_id, to_balance_id, amount, comment=None
    ) -> Transaction:
        try:
            transaction = Transaction()
            transaction.from_balance_id = from_balance_id
            transaction.to_balance_id = to_balance_id
            transaction.amount = amount
            transaction.comment = comment
            db.session.add(transaction)
            from_balance = BalanceQuery.get_balance_by_id(from_balance_id)
            to_balance = BalanceQuery.get_balance_by_id(to_balance_id)
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
        return (
            Transaction.query.filter(Transaction.from_balance_id == balance.id)
            .order_by(Transaction.id.desc())
            .all()
        )

    @staticmethod
    def get_accruals(balance) -> list[Transaction]:
        return (
            Transaction.query.filter(Transaction.to_balance_id == balance.id)
            .order_by(Transaction.id.desc())
            .all()
        )

    @staticmethod
    def create_accrual(balance, amount, comment=None) -> Transaction:
        # user with id 1 will be bank. always. TRUST ME
        # actually not, but just create it if it doesn't exist
        return TransactionQuery.create_transaction(
            1, balance.id, amount, comment=comment
        )

    @staticmethod
    def create_withdraw(balance, amount, comment=None) -> Transaction:
        return TransactionQuery.create_transaction(
            balance.id, 1, amount, comment=comment
        )

    @staticmethod
    def total_count() -> int:
        return Transaction.query.count()

    @staticmethod
    def last_accruals(balance, amount: int = 10) -> list[Transaction]:
        return (
            Transaction.query.filter(Transaction.to_balance_id == balance.id)
            .order_by(Transaction.id.desc())
            .limit(amount)
            .all()
        )
