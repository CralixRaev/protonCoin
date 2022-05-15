from flask_restful import Resource, marshal_with, fields, abort

from db.models.gift import Gift, GiftQuery

gift_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'price': fields.Integer,
}


def abort_if_not_found(gift):
    if not gift:
        abort(404, message=f"Gift with this id does not exist.")


class GiftElement(Resource):
    @marshal_with(gift_fields)
    def get(self, gift_id) -> Gift:
        gift = GiftQuery.get_gift_by_id(gift_id)
        abort_if_not_found(gift)
        return gift


class GiftList(Resource):
    @marshal_with(gift_fields)
    def get(self) -> list[Gift]:
        return GiftQuery.get_all_gifts()

