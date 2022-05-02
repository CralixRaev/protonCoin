import secrets
import string
from datetime import datetime

from flask_login import UserMixin
from transliterate import translit
from werkzeug.security import generate_password_hash, check_password_hash

from db.database import db
from db.models.balances import Balance, BalanceQuery

ALPHABET = string.ascii_letters + string.digits


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
    creation_date = db.Column(db.DateTime, default=datetime.now)

    group = db.relation("Group", back_populates='users')
    balance = db.relation("Balance", back_populates='user', uselist=False)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class UserQuery:
    @staticmethod
    def _create_login(name, surname, patronymic=None):
        name = translit(name, 'ru', reversed=True)
        surname = translit(surname, 'ru', reversed=True)
        if patronymic:
            patronymic = translit(patronymic, 'ru', reversed=True)
        login = surname + name[0]
        if patronymic:
            login += patronymic[0]
        return login.lower()

    @staticmethod
    def _random_password():
        return ''.join(secrets.choice(ALPHABET) for _ in range(8))

    @staticmethod
    def get_user_by_login(login) -> User:
        login = login.lower()
        return User.query.filter((User.email == login) | (User.login == login)).first()

    @staticmethod
    def get_all_users() -> list[User]:
        return User.query.all()

    @staticmethod
    def create_user(name, surname, patronymic=None, email=None, is_admin=False, group=None) -> (
            User, str):
        db.session.rollback()
        user = User()
        user.name = name
        user.surname = surname
        user.email = email
        user.is_admin = is_admin
        user.patronymic = patronymic
        user.group_id = group

        user.balance = BalanceQuery.create_balance(user.id)

        user.login = UserQuery._create_login(name, surname, patronymic)
        password = UserQuery._random_password()
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        return user, password

    @staticmethod
    def update_user(user, name, surname, patronymic=None, email=None, is_admin=False,
                    group=None) -> User:
        db.session.rollback()
        user.name = name
        user.surname = surname
        user.email = email
        user.is_admin = is_admin
        user.patronymic = patronymic
        user.group_id = group

        db.session.commit()
        return user

    @staticmethod
    def new_password(user_id) -> str:
        password = UserQuery._random_password()
        user = User.query.get(user_id)
        user.set_password(password)
        db.session.commit()
        return password

    @staticmethod
    def get_user_by_id(user_id) -> User:
        return User.query.get(user_id)
