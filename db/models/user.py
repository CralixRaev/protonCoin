import logging
import secrets
import string
from datetime import datetime

import sqlalchemy.exc
from flask_login import UserMixin
from sqlalchemy import func
from transliterate import translit
from werkzeug.security import generate_password_hash, check_password_hash

from db.database import db
from db.models.balances import Balance, BalanceQuery
from uploads import avatars

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
    is_teacher = db.Column(db.Boolean, default=False)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"), nullable=True, index=True)
    creation_date = db.Column(db.DateTime, default=datetime.now)
    avatar = db.Column(db.String(128), default="default.png")

    group = db.relation("Group", back_populates='users')
    balance = db.relation("Balance", back_populates='user', uselist=False)
    orders = db.relation("Order", back_populates='user')
    achievements = db.relation("Achievement", back_populates='user')

    @property
    def full_name(self) -> str:
        return f"{self.surname} {self.name} {self.patronymic}"

    @property
    def avatar_path(self) -> str:
        return avatars.url(self.avatar if self.avatar else 'default.png')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password) -> bool:
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
        return login.replace("'", "").lower()

    @staticmethod
    def _random_password():
        return ''.join(secrets.choice(ALPHABET) for _ in range(8))

    @staticmethod
    def get_user_by_login(login) -> User:
        login = login.lower()
        return User.query.filter((User.email == login) | (User.login == login)).first()

    @staticmethod
    def get_all_users() -> list[User]:
        return User.query.order_by(User.patronymic).all()

    @staticmethod
    def search_by_name(full_name, offset=0, limit=10) -> tuple[list[User], int]:
        searched = User.query.filter(
            (User.surname + ' ' + User.name + ' ' + User.patronymic).ilike(
                f"%{full_name}%"))
        return searched.offset(offset).limit(limit).all(), searched.count()

    @staticmethod
    def user_count() -> int:
        return User.query.count()

    @staticmethod
    def get_offset_limit_users(offset=0, limit=10) -> list[User]:
        return User.query.order_by(User.group_id).order_by(User.surname).offset(offset).limit(limit).all()

    @staticmethod
    def create_user(name, surname, patronymic=None, email=None, is_admin=False, is_teacher=False,
                    group=None) -> (
            User, str):
        db.session.rollback()
        user = User()
        user.name = name
        user.surname = surname
        user.email = email
        user.is_admin = is_admin
        user.is_teacher = is_teacher
        user.patronymic = patronymic
        user.group_id = group

        user.balance = BalanceQuery.create_balance(user.id)

        user.login = UserQuery._create_login(name, surname, patronymic)

        password = UserQuery._random_password()
        user.set_password(password)
        try:
            db.session.add(user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()

            user.login += '1'

            db.session.commit()
        return user, password

    @staticmethod
    def update_user(user, name, surname, patronymic=None, email=None, is_admin=False,
                    is_teacher=False,
                    group=None) -> User:
        db.session.rollback()
        user.name = name
        user.surname = surname
        user.email = email
        user.is_admin = is_admin
        user.is_teacher = is_teacher
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
    def update_password(user, password):
        user.set_password(password)
        db.session.commit()

    @staticmethod
    def get_user_by_id(user_id) -> User:
        return User.query.get(user_id)

    @staticmethod
    def update_avatar(user, new_filename):
        user.avatar = new_filename
        db.session.commit()

    @staticmethod
    def update_email(user, email):
        user.email = email
        db.session.commit()

    @staticmethod
    def delete_user(user: User):
        User.query.filter(User.id == user.id).delete()
        db.session.commit()

    @staticmethod
    def find_user(surname, name, patronymic, number, letter) -> User | None:
        return User.query.join(User.group, aliased=True).filter(letter == letter,
                                                                number == number,
                                                                User.surname == surname,
                                                                User.name == name,
                                                                User.patronymic == patronymic).first()
