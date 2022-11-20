from flask_restful import abort, reqparse, marshal
from marshmallow import EXCLUDE, fields, Schema
from sqlalchemy import desc, asc

list_parser = reqparse.RequestParser()
list_parser.add_argument('draw', type=int, help='Used for DataTables, ignore it')
list_parser.add_argument('start', type=int, default=0)
list_parser.add_argument('length', type=int, default=10)


class ListQuery(Schema):
    class Meta:
        unknown = EXCLUDE

    draw = fields.Integer(required=False)
    start = fields.Integer(load_default=0)
    length = fields.Integer(load_default=10)
    search = fields.String(data_key="search[value]")
    order_column_id = fields.String(data_key="order[0][column]")
    order_direction = fields.String(data_key="order[0][dir]")


def abort_if_not_found(obj):
    if not obj:
        abort(404, message=f"Entity with this id does not exist.")


def generate_list_response(args, rows, get_method, count_method, fields, get_api_kwargs: dict):
    order_expr = None
    print(args)
    if 'order_column_id' in args:
        order_expr = rows[int(args['order_column_id'])]
        if args['order_direction'] == 'desc':
            order_expr = tuple(map(lambda x: desc(x), order_expr))
        elif args['order_direction'] == 'asc':
            order_expr = tuple(map(lambda x: asc(x), order_expr))
    count, records = get_method(start=args['start'], length=args['length'],
                                search=args['search'] if 'search' in args else None,
                                order_expr=order_expr, **get_api_kwargs)
    answer = {
        'recordsTotal': count_method(),
        'recordsFiltered': count,
        'data': marshal(records, fields)
    }
    if 'draw' in args:
        answer['draw'] = args['draw']
    return answer
