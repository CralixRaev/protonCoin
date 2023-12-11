from flask import request
from flask_restful import Resource
from sqlalchemy import text

from protonCoin.blueprints.api.utils import ListQuery, generate_list_response
from protonCoin.db.models.criteria import Criteria, CriteriaQuery


class CriteriaList(Resource):
    def get(self) -> dict:
        args = ListQuery().load(request.args)
        rows = [None, ("id",), (text("basis.name"),), ("name",), ("cost",)]
        return generate_list_response(
            args,
            rows,
            CriteriaQuery.get_api,
            CriteriaQuery.total_count,
            Criteria.__json__(),
        )
