from datetime import datetime

from db.database import db
from db.models.gift import Gift
from uploads import gift_images


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    gift_id = db.Column(db.Integer, db.ForeignKey("gift.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    is_issued = db.Column(db.Boolean, nullable=False, default=False)
    is_returned = db.Column(db.Boolean, nullable=False, default=False)
    creation_date = db.Column(db.DateTime, default=datetime.now)

    gift = db.relation("Gift", back_populates='orders')
    user = db.relation("User", back_populates='orders')

    @property
    def status(self) -> str:
        if self.is_issued:
            return "Выдан"
        elif self.is_returned:
            return "Отмена"
        else:
            return "Ожидает обработки"


class OrderQuery:
    @staticmethod
    def create_order(gift_id: int, user_id: int) -> Order:
        db.session.rollback()

        order = Order()
        order.gift_id = gift_id
        order.user_id = user_id
        Gift.query.get(gift_id).stock -= 1

        db.session.add(order)
        db.session.commit()

        return order

    @staticmethod
    def issue_order(order: Order):
        db.session.rollback()

        order.is_issued = True

        db.session.commit()

    @staticmethod
    def return_order(order: Order):
        db.session.rollback()

        order.is_returned = True
        order.gift.stock += 1

        db.session.commit()

    @staticmethod
    def get_awaited_orders() -> list[Order]:
        return Order.query.filter(Order.is_issued == False).filter(
            Order.is_returned == False).all()

    @staticmethod
    def get_order_by_id(order_id: int) -> Order:
        return Order.query.get(order_id)
