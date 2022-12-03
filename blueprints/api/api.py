import flask
from flask import Blueprint
from flask_restful import Api

from blueprints.api.resources.achievement import AchievementList
from blueprints.api.resources.basis import BasisList
from blueprints.api.resources.criteria import CriteriaList
from blueprints.api.resources.gift import GiftList
from blueprints.api.resources.group import GroupList
from blueprints.api.resources.transaction import TransactionList
from blueprints.api.resources.user import UserList

api_blueprint = Blueprint('api', __name__)
# todo: auth
api = Api(api_blueprint)

# api.add_resource(GiftList, '/gifts/')
# api.add_resource(GiftElement, '/gifts/<gift_id>')
api.add_resource(GroupList, '/groups/')
api.add_resource(BasisList, '/basis/')
api.add_resource(CriteriaList, '/criterias/')
api.add_resource(TransactionList, '/transactions/')
api.add_resource(UserList, '/users/')
api.add_resource(AchievementList, '/achievements/', '/achievements/<status>')
api.add_resource(GiftList, '/gifts/')
