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
