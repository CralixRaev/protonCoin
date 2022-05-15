import flask
from flask import Blueprint
from flask_restful import Api

from blueprints.api.resources.gift import GiftList, GiftElement

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

api.add_resource(GiftList, '/gifts/')
api.add_resource(GiftElement, '/gifts/<gift_id>')
