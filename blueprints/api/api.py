import flask
from flask import Blueprint, request
from flask_login import login_required, current_user
from flask_restful import Api

from blueprints.api.resources.achievement import AchievementList
from blueprints.api.resources.basis import BasisList
from blueprints.api.resources.criteria import CriteriaList
from blueprints.api.resources.gift import GiftList
from blueprints.api.resources.group import GroupList
from blueprints.api.resources.news import NewsList
from blueprints.api.resources.order import OrderList
from blueprints.api.resources.transaction import TransactionList
from blueprints.api.resources.user import UserList
from util import teacher_or_admin_required

api_blueprint = Blueprint('api', __name__)
@api_blueprint.before_request
def before_request():
    if request.endpoint != 'api.criterialist':
        if not current_user.is_authenticated or not (current_user.is_teacher or current_user.is_admin):
            flask.abort(403)


api = Api(api_blueprint)
api.add_resource(GroupList, '/groups/')
api.add_resource(BasisList, '/basis/')
api.add_resource(CriteriaList, '/criterias/')
api.add_resource(TransactionList, '/transactions/')
api.add_resource(UserList, '/users/')
api.add_resource(AchievementList, '/achievements/', '/achievements/<status>')
api.add_resource(GiftList, '/gifts/')
api.add_resource(OrderList, '/orders/')
api.add_resource(NewsList, '/news/')
