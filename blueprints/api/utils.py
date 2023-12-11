from flask_restful import abort, marshal
from marshmallow import EXCLUDE, fields, Schema
from sqlalchemy import desc, asc


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
        abort(404, message="Entity with this id does not exist.")


def generate_list_response(
    args,
    rows,
    get_method,
    count_method,
    fields,
    get_api_kwargs: dict | None = None,
    total_count_kwargs: dict | None = None,
):
    if total_count_kwargs is None:
        total_count_kwargs = {}
    if get_api_kwargs is None:
        get_api_kwargs = {}
    order_expr = None
    if "order_column_id" in args:
        order_expr = rows[int(args["order_column_id"])]
        if args["order_direction"] == "desc":
            order_expr = tuple(map(desc, order_expr))
        elif args["order_direction"] == "asc":
            order_expr = tuple(map(asc, order_expr))
    count, records = get_method(
        start=args["start"],
        length=args["length"],
        search=args.get("search", None),
        order_expr=order_expr,
        **get_api_kwargs,
    )
    answer = {
        "recordsTotal": count_method(**total_count_kwargs),
        "recordsFiltered": count,
        "data": marshal(records, fields),
    }
    if "draw" in args:
        answer["draw"] = args["draw"]
    return answer
