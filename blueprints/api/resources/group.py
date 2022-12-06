from flask import request
from flask_restful import Resource, marshal_with, abort, marshal
from marshmallow import Schema, fields, EXCLUDE
from sqlalchemy import types
from sqlalchemy.sql import functions, expression

from blueprints.api.utils import abort_if_not_found, ListQuery, generate_list_response
from db.models.group import Group, GroupQuery


class GroupElement(Resource):
    @marshal_with(Group.__json__())
    def get(self, group_id) -> Group:
        group = GroupQuery.get_group_by_id(group_id)
        abort_if_not_found(group)
        return group


class GroupList(Resource):
    def get(self) -> dict:
        args = ListQuery().load(request.args)
        rows = [None, (Group.id,), (Group.stage, Group.letter)]
        return generate_list_response(args, rows, GroupQuery().get_api, GroupQuery().total_count,
                                      Group.__json__())