from db.database import db


class Gift(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)

    @property
    def image_file(self):
        return f'{self.id}.png'


class GiftQuery:
    @staticmethod
    def get_all_gifts() -> list[Gift]:
        return Gift.query.all()

    @staticmethod
    def create_gift(name, description, price) -> Gift:
        gift = Gift()
        gift.name = name
        gift.description = description
        gift.price = price

        db.session.add(gift)
        db.session.commit()
        return gift

    @staticmethod
    def update_gift(gift, name, description, price) -> Gift:
        gift.name = name
        gift.description = description
        gift.price = price
        db.session.commit()
        return gift

    @staticmethod
    def get_gift_by_id(gift_id) -> Gift:
        return Gift.query.get(gift_id)
