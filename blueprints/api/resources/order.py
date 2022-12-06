from flask import request
from flask_restful import Resource
from sqlalchemy import text
from sqlalchemy.sql import functions

from blueprints.api.utils import abort_if_not_found, list_parser, ListQuery, generate_list_response
from db.models.achievement import AchievementQuery, Achievement
from db.models.basis import BasisQuery, Basis
from db.models.criteria import Criteria, CriteriaQuery
from db.models.group import Group, GroupQuery
from db.models.order import Order, OrderQuery
from db.models.user import User, UserQuery
from util import is_teacher_to_bool


class OrderList(Resource):
    def get(self) -> dict:
        args = ListQuery().load(request.args)
        rows = [('id',), ('gift_id',), ('status',), ('user_id',), ('creation_date',), None]
        return generate_list_response(args, rows, OrderQuery.get_api, OrderQuery.total_count,
                                      Order.__json__())
