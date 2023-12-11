from flask import request
from flask_restful import Resource

from protonCoin.blueprints.api.utils import ListQuery, generate_list_response
from protonCoin.db.models.order import Order, OrderQuery


class OrderList(Resource):
    def get(self) -> dict:
        args = ListQuery().load(request.args)
        rows = [
            ("id",),
            ("gift_id",),
            ("status",),
            ("user_id",),
            ("creation_date",),
            None,
        ]
        return generate_list_response(
            args, rows, OrderQuery.get_api, OrderQuery.total_count, Order.__json__()
        )
