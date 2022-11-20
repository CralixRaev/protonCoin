from flask_restful import fields
from sqlalchemy import types
from sqlalchemy.sql import functions, expression

from db.database import db
from util import ABCQuery


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    stage = db.Column(db.Integer, nullable=False)
    letter = db.Column(db.String(8), nullable=False)

    users = db.relationship('User', back_populates='group', order_by='User.surname')

    @property
    def name(self) -> str:
        return f'{self.stage}{self.letter}'

    @staticmethod
    def __json__() -> dict:
        _json = {
            'id': fields.Integer(),
            'stage': fields.Integer(),
            'letter': fields.String()
        }
        return _json


class GroupQuery:
    @staticmethod
    def total_count() -> int:
        return Group.query.count()

    @staticmethod
    def get_all_groups() -> list[Group]:
        return Group.query.all()

    @staticmethod
    def get_api(start: int = 0, length: int = 10, search: str | None = None, order_expr=None) -> (
            int, list[Group]):
        groups_query = Group.query
        count = groups_query.count()
        if search:
            groups_query = groups_query.filter(
                functions.concat(expression.cast(Group.stage, types.Unicode), Group.letter).ilike(
                    f'%{search}%'))
            count = groups_query.count()
        print(order_expr)
        if order_expr is not None:
            groups_query = groups_query.order_by(*order_expr)
        groups_query = groups_query.limit(length).offset(start)
        return count, groups_query.all()

    @staticmethod
    def create_group(stage: int, letter) -> Group:
        db.session.rollback()
        group = Group()
        group.stage = stage
        group.letter = letter
        db.session.add(group)
        db.session.commit()
        return group

    @staticmethod
    def get_group_by_id(group_id) -> Group:
        return Group.query.get(group_id)

    @staticmethod
    def get_group_by_stage_letter(stage, letter) -> Group:
        return Group.query.filter(Group.stage == stage, Group.letter == letter).first()

    @staticmethod
    def update_group(group: Group, stage: int, letter: str) -> Group:
        db.session.rollback()

        group.stage = stage
        group.letter = letter

        db.session.commit()
        return group

    @staticmethod
    def delete_group(group: Group):
        Group.query.filter(Group.id == group.id).delete()
        db.session.commit()
