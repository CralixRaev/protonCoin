from flask import request
from flask_restful import Resource
from sqlalchemy.sql import functions

from blueprints.api.utils import abort_if_not_found, list_parser, ListQuery, generate_list_response
from db.models.achievement import AchievementQuery, Achievement
from db.models.basis import BasisQuery, Basis
from db.models.criteria import Criteria, CriteriaQuery
from db.models.group import Group, GroupQuery
from db.models.user import User, UserQuery


class AchievementList(Resource):
    def get(self, status: str | None = None) -> dict:
        if status:
            print(status)
        args = ListQuery().load(request.args)
        rows = [("id",), ("user_id",), ("criteria_id",), None, None, ('status', )]
        return generate_list_response(args, rows, AchievementQuery.get_api, AchievementQuery.total_count,
                                      Achievement.__json__(), get_api_kwargs={'status': status})
