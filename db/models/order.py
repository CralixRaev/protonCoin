from datetime import datetime
from enum import Enum

from flask_restful import fields

from db.database import db
from db.models.gift import Gift
from db.models.transaction import TransactionQuery
from db.models.user import User


class OrderStatusEnum(Enum):
    created = "created"
    delivered = "delivered"
    cancelled = "cancelled"
    cancelled_user = "cancelled_user"


STATUS_TO_STRING = {
    OrderStatusEnum.created: "Создан",
    OrderStatusEnum.delivered: "Доставлен",
    OrderStatusEnum.cancelled: "Отменён",
    OrderStatusEnum.cancelled_user: "Отменён пользователем",
}


class Order(db.Model):
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True
    )
    gift_id = db.Column(db.Integer, db.ForeignKey("gift.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(
        db.Enum(OrderStatusEnum), default=OrderStatusEnum.created, nullable=False
    )
    creation_date = db.Column(db.DateTime, default=datetime.now)

    gift = db.relation("Gift", back_populates="orders")
    user = db.relation("User", back_populates="orders")

    @property
    def status_translation(self) -> str:
        return STATUS_TO_STRING[self.status]

    @property
    def cancellation_available(self) -> bool:
        return self.status == OrderStatusEnum.created

    @staticmethod
    def __json__() -> dict:
        _json = {
            "id": fields.Integer(),
            "gift": fields.Nested(Gift.__json__()),
            "user": fields.Nested(User.__json__()),
            "status": fields.FormattedString("{status.value}"),
            "status_translation": fields.String(),
            "creation_date": fields.DateTime(dt_format="iso8601"),
        }
        return _json


class OrderQuery:
    @staticmethod
    def total_count() -> int:
        return Order.query.count()

    @staticmethod
    def get_api(
        start: int = 0, length: int = 10, search: str | None = None, order_expr=None
    ) -> (int, list[Gift]):
        order_query = Order.query
        count = order_query.count()
        if search:
            order_query = order_query.filter()
            count = order_query.count()
        if order_expr is not None:
            order_query = order_query.order_by(*order_expr)
        order_query = order_query.limit(length).offset(start)
        return count, order_query.all()

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
    def deliver_order(order: Order):
        db.session.rollback()

        order.status = OrderStatusEnum.delivered

        db.session.commit()

    @staticmethod
    def cancel_order(order: Order):
        db.session.rollback()

        order.status = OrderStatusEnum.cancelled
        TransactionQuery.create_accrual(
            order.user.balance, order.gift.price, f"Возврат за заказ №{order.id}"
        )

        db.session.commit()

    @staticmethod
    def get_awaited_orders() -> list[Order]:
        return (
            Order.query.filter(Order.is_issued is False)
            .filter(Order.is_returned is False)
            .all()
        )

    @staticmethod
    def get_order_by_id(order_id: int) -> Order:
        return Order.query.get(order_id)

    @staticmethod
    def order_by_user(user_id: int) -> list[Order]:
        return (
            Order.query.filter(Order.user_id == user_id).order_by(Order.id.desc()).all()
        )

    @staticmethod
    def cancel_order_user(order: Order):
        db.session.rollback()

        order.status = OrderStatusEnum.cancelled_user
        order.gift.stock += 1
        TransactionQuery.create_accrual(
            order.user.balance, order.gift.price, f"Возврат за заказ №{order.id}"
        )

        db.session.commit()
