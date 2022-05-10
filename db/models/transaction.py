from datetime import datetime

from db.database import db


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
        transaction = Transaction()
        transaction.from_balance_id = from_balance_id
        transaction.to_balance_id = to_balance_id
        transaction.amount = amount
        transaction.comment = comment
        # TODO: commit once to ensure what transaction is completed successfully
        db.session.add(transaction)
        db.session.commit()
        if not transaction.from_balance.is_bank:
            transaction.from_balance.amount -= amount

        if not transaction.to_balance.is_bank:
            transaction.to_balance.amount += amount
        db.session.commit()
        return transaction

    @staticmethod
    def get_withdraws(balance) -> list[Transaction]:
        return Transaction.query.filter(Transaction.from_balance_id == balance.id).all()

    @staticmethod
    def get_accruals(balance) -> list[Transaction]:
        return Transaction.query.filter(Transaction.to_balance_id == balance.id).all()
