from flask import request
from flask_restful import Resource
from sqlalchemy.sql import functions

from blueprints.api.utils import abort_if_not_found, list_parser, ListQuery, generate_list_response
from db.models.basis import BasisQuery, Basis
from db.models.criteria import Criteria, CriteriaQuery
from db.models.group import Group, GroupQuery
from db.models.user import User, UserQuery


class UserList(Resource):
    def get(self) -> dict:
        args = ListQuery().load(request.args)
        rows = [("group_id", "surname"), ("id",), ("surname",), ("basis.name",), ("cost",)]
        return generate_list_response(args, rows, UserQuery.get_api, UserQuery.total_count,
                                      User.__json__())
