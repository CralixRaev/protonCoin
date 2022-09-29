from flask import current_app

from db.database import db


class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, unique=True,
                        index=True)
    amount = db.Column(db.Integer, nullable=False, default=0)

    user = db.relationship('User', back_populates='balance', uselist=False)

    @property
    def is_bank(self) -> bool:
        return False if self.user else True

    @property
    def holder_name(self) -> str:
        return 'ПротонБанк' if self.is_bank else self.user.full_name

    def __str__(self) -> str:
        return f"{self.holder_name}: {self.amount if self.user_id else '∞'}"

    def __repr__(self) -> str:
        return self.__str__()


class BalanceQuery:
    @staticmethod
    def get_all_balances() -> list[Balance]:
        return Balance.query.all()

    @staticmethod
    def get_balance_by_id(balance_id: int) -> Balance:
        return Balance.query.filter(Balance.id == balance_id).first()

    @staticmethod
    def ensure_bank_balance():
        if not Balance.query.filter(Balance.user_id == None).first():
            current_app.logger.error("Default balance was not present, creating a new one")
            balance = Balance()
            db.session.add(balance)
            db.session.commit()

    @staticmethod
    def create_balance(user_id: int, commit=False) -> Balance:
        balance = Balance()
        balance.user_id = user_id
        db.session.add(balance)
        if commit:
            db.session.commit()
        return balance

    @staticmethod
    def get_bank():
        # TODO: cache this shit
        return Balance.query.filter(Balance.user_id == None).first()

    @staticmethod
    def top_balances(number: int = 10) -> list[Balance]:
        return Balance.query.filter(Balance.amount > 0).order_by(Balance.amount.desc()).limit(number).all()