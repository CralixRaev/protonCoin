from flask import request
from flask_restful import Resource

from protonCoin.blueprints.api.utils import ListQuery, generate_list_response
from protonCoin.db.models.balances import Balance
from protonCoin.db.models.user import User, UserQuery
from protonCoin.util import is_teacher_to_bool


class UserList(Resource):
    def get(self) -> dict:
        args = ListQuery().load(request.args)
        rows = [
            ("group_id", "surname"),
            ("id",),
            ("surname",),
            ("group_id",),
            (Balance.amount,),
        ]
        return generate_list_response(
            args,
            rows,
            UserQuery.get_api,
            UserQuery.total_count,
            User.__json__(),
            get_api_kwargs={"is_teacher": is_teacher_to_bool()},
            total_count_kwargs={"is_teacher": is_teacher_to_bool()},
        )
