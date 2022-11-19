from flask import request
from flask_restful import Resource, marshal_with, abort, marshal
from marshmallow import Schema, fields, EXCLUDE
from sqlalchemy import types
from sqlalchemy.sql import functions, expression

from blueprints.api.utils import abort_if_not_found, list_parser
from db.models.group import Group, GroupQuery


class GroupListQuery(Schema):
    class Meta:
        unknown = EXCLUDE

    draw = fields.Integer(required=False)
    start = fields.Integer(load_default=0)
    length = fields.Integer(load_default=10)
    search = fields.String(data_key="search[value]")
    order_column_id = fields.String(data_key="order[0][column]")
    order_direction = fields.String(data_key="order[0][dir]")


class GroupElement(Resource):
    @marshal_with(Group.__json__())
    def get(self, group_id) -> Group:
        group = GroupQuery.get_group_by_id(group_id)
        abort_if_not_found(group)
        return group


class GroupList(Resource):
    def get(self) -> dict:
        args = GroupListQuery().load(request.args)
        rows = [(Group.id,), (Group.stage, Group.letter)]
        order_expr = None
        if 'order_column_id' in args:
            order_expr = rows[int(args['order_column_id'])]
            if args['order_direction'] == 'desc':
                order_expr = tuple(map(lambda x: x.desc(), order_expr))
            elif args['order_direction'] == 'asc':
                order_expr = tuple(map(lambda x: x.asc(), order_expr))
        count, records = GroupQuery.get_groups(start=args['start'], length=args['length'],
                                               search=args['search'] if 'search' in args else None,
                                               order_expr=order_expr)
        answer = {
            'recordsTotal': GroupQuery.total_count(),
            'recordsFiltered': count,
            'data': marshal(records, Group.__json__())
        }
        if 'draw' in args:
            answer['draw'] = args['draw']
        return answer
