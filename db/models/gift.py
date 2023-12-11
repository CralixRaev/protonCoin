from flask_restful import fields

from db.database import db
from uploads import gift_images


class Gift(db.Model):
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True
    )
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)
    promo_price = db.Column(db.Integer, nullable=True, default=None)
    image = db.Column(db.String(1024), default="default.jpeg")
    stock = db.Column(db.Integer, default=0)

    orders = db.relation("Order", back_populates="gift")

    @property
    def image_file(self):
        return gift_images.url(self.image if self.image else "default.jpeg")

    @property
    def in_stock(self) -> bool:
        if self.stock is None:
            self.stock = 0
            db.session.commit()
        return self.stock > 0

    @staticmethod
    def __json__() -> dict:
        _json = {
            "id": fields.Integer(),
            "name": fields.String(),
            "description": fields.String(),
            "stock": fields.Integer(),
            "price": fields.Integer(),
            "promo_price": fields.Integer(),
            "image_file": fields.String(),
        }
        return _json


class GiftQuery:
    @staticmethod
    def get_all_gifts(order_by=Gift.price.desc()) -> list[Gift]:
        qr = Gift.query.order_by(Gift.stock == 0, order_by)
        return qr.all()

    @staticmethod
    def create_gift(name, description, price, image_path, promo_price) -> Gift:
        gift = Gift()
        gift.name = name
        gift.description = description
        gift.price = price
        gift.promo_price = promo_price
        if image_path:
            gift.image = image_path

        db.session.add(gift)
        db.session.commit()
        return gift

    @staticmethod
    def total_count() -> int:
        return Gift.query.count()

    @staticmethod
    def get_api(
        start: int = 0, length: int = 10, search: str | None = None, order_expr=None
    ) -> (int, list[Gift]):
        gift_query = Gift.query
        count = gift_query.count()
        if search:
            gift_query = gift_query.filter(Gift.name.ilike(f"%{search}%"))
            count = gift_query.count()
        if order_expr is not None:
            gift_query = gift_query.order_by(*order_expr)
        gift_query = gift_query.limit(length).offset(start)
        return count, gift_query.all()

    @staticmethod
    def update_gift(
        gift, name, description, price, image_path, stock, promo_price: int | None
    ) -> Gift:
        gift.name = name
        gift.description = description
        gift.price = price
        gift.promo_price = promo_price
        if image_path:
            gift.image = image_path
        gift.stock = stock
        db.session.commit()
        return gift

    @staticmethod
    def get_gift_by_id(gift_id) -> Gift:
        return Gift.query.get(gift_id)

    @staticmethod
    def delete_gift(gift: Gift):
        Gift.query.filter(Gift.id == gift.id).delete()
        db.session.commit()
