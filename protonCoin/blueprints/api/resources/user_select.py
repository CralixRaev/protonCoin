from flask import request
from flask_restful import Resource

from protonCoin.db.models.user import UserQuery


class UserSelectList(Resource):
    def get(self) -> dict:
        page = int(request.args.get("page", 0))
        count, items = UserQuery.get_api(
            25 * page, 25, request.args.get("term"), order_expr=("surname",)
        )
        return {
            "results": [{"id": 1, "text": "ПротоБанк - ∞"}]
            + [
                {
                    "id": item.balance.id,
                    "text": f"{item.full_name} - {item.balance.amount}",
                }
                for item in items
            ],
            "pagination": {"more": count > (25 * page + 25)},
        }
