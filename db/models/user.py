from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from db.database import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    login = db.Column(db.String(32), nullable=False, unique=True, index=True)
    email = db.Column(db.String(64), nullable=True, unique=True, index=True)
    name = db.Column(db.String(32), nullable=False)
    surname = db.Column(db.String(32), nullable=False)
    patronymic = db.Column(db.String(32), nullable=True)
    hashed_password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    group_id = db.Column(db.Integer, db.ForeignKey("group.id"), nullable=True, index=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class UserQuery:
    @staticmethod
    def get_user_by_login(login) -> User:
        return User.query.filter((User.email == login) | (User.login == login)).first()

    @staticmethod
    def get_all_users() -> list[User]:
        return User.query.all()
