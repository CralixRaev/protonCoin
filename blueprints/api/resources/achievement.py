from flask import request
from flask_restful import Resource
from sqlalchemy import text
from sqlalchemy.sql import functions

from blueprints.api.utils import abort_if_not_found, ListQuery, generate_list_response
from db.models.achievement import AchievementQuery, Achievement
from db.models.basis import BasisQuery, Basis
from db.models.criteria import Criteria, CriteriaQuery
from db.models.group import Group, GroupQuery
from db.models.user import User, UserQuery
from util import is_teacher_to_bool


class AchievementList(Resource):
    def get(self, status: str | None = None) -> dict:
        args = ListQuery().load(request.args)
        rows = [(text("achievement.id"),), (text("achievement.user_id"),), (text("achievement.criteria_id"),), None, None, (text('achievement.status'), )]
        return generate_list_response(args, rows, AchievementQuery.get_api, AchievementQuery.total_count,
                                      Achievement.__json__(), get_api_kwargs={'status': status, 'is_teacher': is_teacher_to_bool()},
                                      total_count_kwargs={'is_teacher': is_teacher_to_bool()})
