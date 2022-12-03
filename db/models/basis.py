from flask_restful import fields
from sqlalchemy.sql import functions, expression

from db.database import db
from util import ABCQuery


class Basis(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    name = db.Column(db.String(255))

    criteria = db.relation("Criteria", back_populates='basis')

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def __json__() -> dict:
        _json = {
            'id': fields.Integer(),
            'name': fields.String(),
        }
        return _json


class BasisQuery:
    @staticmethod
    def total_count() -> int:
        return Basis.query.count()

    @staticmethod
    def get_api(start: int = 0, length: int = 10, search: str | None = None, order_expr=None) -> (
            int, list[Basis]):
        basis_query = Basis.query
        count = basis_query.count()
        if search:
            basis_query = basis_query.filter(Basis.name.ilike(f'%{search}%'))
            count = basis_query.count()
        if order_expr is not None:
            basis_query = basis_query.order_by(*order_expr)
        basis_query = basis_query.limit(length).offset(start)
        return count, basis_query.all()

    @staticmethod
    def get_all_basises() -> list[Basis]:
        return Basis.query.all()

    @staticmethod
    def create_basis(name) -> Basis:
        basis = Basis()
        basis.name = name
        db.session.add(basis)
        db.session.commit()
        return basis
