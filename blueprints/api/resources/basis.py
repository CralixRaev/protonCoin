from flask import request
from flask_restful import Resource, marshal_with, abort, marshal
from marshmallow import Schema, fields, EXCLUDE
from sqlalchemy import types
from sqlalchemy.sql import functions, expression

from blueprints.api.utils import abort_if_not_found, ListQuery, generate_list_response
from db.models.basis import BasisQuery, Basis
from db.models.group import Group, GroupQuery


class BasisList(Resource):
    def get(self) -> dict:
        args = ListQuery().load(request.args)
        rows = [None, (Basis.id,), (Basis.name,)]
        return generate_list_response(args, rows, BasisQuery.get_api, BasisQuery.total_count,
                                      Basis.__json__())
