from flask import request
from flask_restful import Resource

from blueprints.api.utils import abort_if_not_found, list_parser, ListQuery, generate_list_response
from db.models.basis import BasisQuery, Basis
from db.models.criteria import Criteria, CriteriaQuery
from db.models.group import Group, GroupQuery


class CriteriaList(Resource):
    def get(self) -> dict:
        args = ListQuery().load(request.args)
        rows = [None, ("id",), ("name",), ("basis.name",), ("cost",)]
        return generate_list_response(args, rows, CriteriaQuery.get_api, CriteriaQuery.total_count,
                                      Criteria.__json__())
