from flask import request
from flask_restful import Resource

from protonCoin.blueprints.api.utils import ListQuery, generate_list_response
from protonCoin.db.models.gift import Gift, GiftQuery


class GiftList(Resource):
    def get(self) -> dict:
        args = ListQuery().load(request.args)
        rows = [None, ("id",), ("name",), ("price",), ("stock",)]
        return generate_list_response(
            args, rows, GiftQuery.get_api, GiftQuery.total_count, Gift.__json__()
        )
