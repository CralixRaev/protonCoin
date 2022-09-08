from db.database import db
from uploads import gift_images


class Gift(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)
    image = db.Column(db.String(1024), default="default.jpeg")

    orders = db.relation("Order", back_populates='gift')

    @property
    def image_file(self):
        return gift_images.url(self.image if self.image else 'default.jpeg')


class GiftQuery:
    @staticmethod
    def get_all_gifts() -> list[Gift]:
        return Gift.query.order_by(Gift.price.desc()).all()

    @staticmethod
    def create_gift(name, description, price, image_path) -> Gift:
        gift = Gift()
        gift.name = name
        gift.description = description
        gift.price = price
        gift.image = image_path

        db.session.add(gift)
        db.session.commit()
        return gift

    @staticmethod
    def update_gift(gift, name, description, price, image_path) -> Gift:
        gift.name = name
        gift.description = description
        gift.price = price
        gift.image = image_path
        db.session.commit()
        return gift

    @staticmethod
    def get_gift_by_id(gift_id) -> Gift:
        return Gift.query.get(gift_id)
