from flask import request
from flask_restful import Resource

from protonCoin.blueprints.api.utils import ListQuery, generate_list_response
from protonCoin.db.models.basis import BasisQuery, Basis


class BasisList(Resource):
    def get(self) -> dict:
        args = ListQuery().load(request.args)
        rows = [None, (Basis.id,), (Basis.name,)]
        return generate_list_response(
            args, rows, BasisQuery.get_api, BasisQuery.total_count, Basis.__json__()
        )
