from flask import request
from flask_restful import Resource
from sqlalchemy import text, desc
from sqlalchemy.sql import functions

from blueprints.api.utils import abort_if_not_found, ListQuery, generate_list_response
from db.models.balances import Balance
from db.models.basis import BasisQuery, Basis
from db.models.criteria import Criteria, CriteriaQuery
from db.models.group import Group, GroupQuery
from db.models.user import User, UserQuery
from util import is_teacher_to_bool


class UserList(Resource):
    def get(self) -> dict:
        args = ListQuery().load(request.args)
        rows = [("group_id", "surname"), ("id",), ('surname',), ('group_id',), (Balance.amount,)]
        return generate_list_response(args, rows, UserQuery.get_api, UserQuery.total_count,
                                      User.__json__(), get_api_kwargs={'is_teacher': is_teacher_to_bool()},
                                      total_count_kwargs={'is_teacher': is_teacher_to_bool()})
