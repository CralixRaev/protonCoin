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


class UserSelectList(Resource):
    def get(self) -> dict:
        page = int(request.args.get("page", 0))
        count, items = UserQuery.get_api(25 * page, 25, request.args.get("term"), order_expr=("surname",))
        return {
            "results": [{"id": 1, "text": f"ПротоБанк - ∞"}] + [{
                "id": item.balance.id,
                "text": f"{item.full_name} - {item.balance.amount}",
            } for item in items],
            "pagination": {
                "more": True if count > (25 * page + 25) else False
            }
        }