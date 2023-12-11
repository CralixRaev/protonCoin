from flask import request
from flask_restful import Resource
from sqlalchemy import text

from protonCoin.blueprints.api.utils import ListQuery, generate_list_response
from protonCoin.db.models.achievement import AchievementQuery, Achievement
from protonCoin.util import is_teacher_to_bool


class AchievementList(Resource):
    def get(self, status: str | None = None) -> dict:
        args = ListQuery().load(request.args)
        rows = [
            (text("achievement.id"),),
            (text("achievement.user_id"),),
            (text("achievement.criteria_id"),),
            None,
            None,
            (text("achievement.status"),),
        ]
        return generate_list_response(
            args,
            rows,
            AchievementQuery.get_api,
            AchievementQuery.total_count,
            Achievement.__json__(),
            get_api_kwargs={"status": status, "is_teacher": is_teacher_to_bool()},
            total_count_kwargs={"is_teacher": is_teacher_to_bool()},
        )
