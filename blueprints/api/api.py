import flask
from flask import Blueprint
from flask_restful import Api

from blueprints.api.resources.gift import GiftList, GiftElement
from blueprints.api.resources.group import GroupList

api_blueprint = Blueprint('api', __name__)
# todo: auth
api = Api(api_blueprint)

# api.add_resource(GiftList, '/gifts/')
# api.add_resource(GiftElement, '/gifts/<gift_id>')
api.add_resource(GroupList, '/groups/')
api.add_resource(GiftElement, '/groups/<group_id>')
