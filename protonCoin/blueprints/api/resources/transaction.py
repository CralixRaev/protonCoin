from flask import request
from flask_restful import Resource
from sqlalchemy import text

from protonCoin.blueprints.api.utils import ListQuery, generate_list_response
from protonCoin.db.models.transaction import TransactionQuery, Transaction


class TransactionList(Resource):
    def get(self) -> dict:
        args = ListQuery().load(request.args)
        rows = [
            (text("transaction.id"),),
            ("from_balance_id",),
            ("to_balance_id",),
            (text("transaction.amount"),),
            None,
            (text("transaction.creation_date"),),
        ]
        return generate_list_response(
            args,
            rows,
            TransactionQuery.get_api,
            TransactionQuery.total_count,
            Transaction.__json__(),
        )
