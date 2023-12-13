from datetime import datetime
from uuid import uuid4

import sqlalchemy.exc
from flask_login import UserMixin, current_user
from flask_restful import fields
from transliterate import translit
from werkzeug.security import generate_password_hash, check_password_hash

from protonCoin.db.database import db
from protonCoin.db.models.balances import Balance, BalanceQuery
from protonCoin.db.models.group import Group
from protonCoin.uploads import avatars
from protonCoin.util import random_password


class User(db.Model, UserMixin):
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True
    )
    login = db.Column(db.String(32), nullable=False, unique=True, index=True)
    nickname = db.Column(db.String(16), nullable=True, unique=True, index=True)
    email = db.Column(db.String(64), nullable=True, unique=True, index=True)
    name = db.Column(db.String(32), nullable=False)
    surname = db.Column(db.String(32), nullable=False)
    patronymic = db.Column(db.String(32), nullable=True)
    hashed_password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_teacher = db.Column(db.Boolean, default=False)
    group_id = db.Column(
        db.Integer, db.ForeignKey("group.id"), nullable=True, index=True
    )
    creation_date = db.Column(db.DateTime, default=datetime.now)
    last_auth = db.Column(db.DateTime, default=None, nullable=True)
    avatar = db.Column(db.String(128), default="default.png")
    alternative_id = db.Column(db.String(36), nullable=False, default=uuid4)

    group = db.relation("Group", back_populates="users")
    balance = db.relation("Balance", back_populates="user", uselist=False)
    orders = db.relation("Order", back_populates="user")

    def get_id(self) -> str:
        return str(self.alternative_id)

    @property
    def full_name(self) -> str:
        return f"{self.surname} {self.name} {self.patronymic}"

    @property
    def avatar_path(self) -> str:
        return avatars.url(self.avatar if self.avatar else "default.png")

    def set_password(self, password):
        self.alternative_id = str(uuid4())
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.hashed_password, password)

    @staticmethod
    def __json__() -> dict:
        _json = {
            "id": fields.Integer(),
            "login": fields.String(),
            "email": fields.String(),
            "name": fields.String(),
            "surname": fields.String(),
            "patronymic": fields.String(),
            "avatar_path": fields.String(),
            "group": fields.Nested(Group.__json__()),
            "balance": fields.Nested(Balance.__json__()),
        }
        return _json


class UserQuery:
    @staticmethod
    def total_count(is_teacher: bool = False) -> int:
        if is_teacher:
            return User.query.filter(User.group_id == current_user.group_id).count()
        else:
            return User.query.count()

    @staticmethod
    def _create_login(name, surname, patronymic=None):
        name = translit(name, "ru", reversed=True)
        surname = translit(surname, "ru", reversed=True)
        if patronymic:
            patronymic = translit(patronymic, "ru", reversed=True)
        login = surname + name[0]
        if patronymic:
            login += patronymic[0]
        return login.replace("'", "").lower()

    @staticmethod
    def get_user_by_login(login: str) -> User:
        login = login.strip().lower()
        return User.query.filter((User.email == login) | (User.login == login)).first()

    @staticmethod
    def get_user_by_email(email: str) -> User:
        email = email.strip().lower()
        return User.query.filter(User.email == email).first()

    @staticmethod
    def get_api(
        start: int = 0,
        length: int = 10,
        search: str | None = None,
        order_expr=None,
        is_teacher=False,
    ) -> (int, list[User]):
        user_query = User.query.join(Balance)
        if is_teacher:
            user_query = user_query.filter(User.group_id == current_user.group_id)
        count = user_query.count()
        if search:
            user_query = user_query.filter(
                (User.surname + " " + User.name + " " + User.patronymic).ilike(
                    f"%{search}%"
                )
            )
            count = user_query.count()
        if order_expr is not None:
            user_query = user_query.order_by(*order_expr)
        user_query = user_query.limit(length).offset(start)
        return count, user_query.all()

    @staticmethod
    def get_all_users() -> list[User]:
        return User.query.order_by(User.patronymic).all()

    @staticmethod
    def search_by_name(full_name, offset=0, limit=10) -> tuple[list[User], int]:
        searched = User.query.filter(
            (User.surname + " " + User.name + " " + User.patronymic).ilike(
                f"%{full_name}%"
            )
        )
        return searched.offset(offset).limit(limit).all(), searched.count()

    @staticmethod
    def user_count(is_teacher: bool = False) -> int:
        return UserQuery.total_count(is_teacher)

    @staticmethod
    def set_nickname(user: User, nickname: str):
        if not user.nickname:
            user.nickname = nickname
        else:
            raise ValueError("cannot update nickname if it already set")
        db.session.commit()

    @staticmethod
    def get_offset_limit_users(offset=0, limit=10) -> list[User]:
        return (
            User.query.order_by(User.group_id)
            .order_by(User.surname)
            .offset(offset)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create_user(
        name,
        surname,
        patronymic=None,
        email=None,
        is_admin=False,
        is_teacher=False,
        group=None,
    ) -> (User, str):
        # FIXME: RENAME GROUP TO GROUP_ID!!!
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

        password = random_password()
        user.set_password(password)
        try:
            db.session.add(user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()

            user.login += "1"
            try:
                db.session.add(user)
                db.session.commit()
            except sqlalchemy.exc.IntegrityError:
                db.session.rollback()

                user.login = user.login[:-1] + "2"
                db.session.add(user)
                db.session.commit()
        return user, password

    @staticmethod
    def update_user(
        user,
        name,
        surname,
        patronymic=None,
        email=None,
        is_admin=False,
        is_teacher=False,
        group=None,
    ) -> User:
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
        password = random_password()
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
    def update_auth_time(user: User):
        user.last_auth = datetime.now()
        db.session.commit()

    @staticmethod
    def find_user(surname, name, patronymic: str | None = None) -> User | None:
        if patronymic:
            user = User.query.filter(
                User.surname == surname,
                User.name == name,
                User.patronymic == patronymic,
            )
        else:
            user = User.query.filter(User.surname == surname, User.name == name)
        if user.count() > 1:
            return None
        else:
            return user.first()
