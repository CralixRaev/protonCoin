from db.database import db


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    stage = db.Column(db.Integer, nullable=False)
    letter = db.Column(db.String(8), nullable=False)

    users = db.relationship('User', backref='groups', lazy=True)
