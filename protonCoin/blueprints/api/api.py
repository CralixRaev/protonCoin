import flask
from flask import Blueprint, request
from flask_login import current_user
from flask_restful import Api

from protonCoin.blueprints.api.resources.achievement import AchievementList
from protonCoin.blueprints.api.resources.basis import BasisList
from protonCoin.blueprints.api.resources.criteria import CriteriaList
from protonCoin.blueprints.api.resources.gift import GiftList
from protonCoin.blueprints.api.resources.group import GroupList
from protonCoin.blueprints.api.resources.news import NewsList
from protonCoin.blueprints.api.resources.order import OrderList
from protonCoin.blueprints.api.resources.transaction import TransactionList
from protonCoin.blueprints.api.resources.user import UserList
from protonCoin.blueprints.api.resources.user_select import UserSelectList

api_blueprint = Blueprint("api", __name__)


@api_blueprint.before_request
def before_request():
    if request.endpoint != "api.criterialist":
        if not current_user.is_authenticated or not (
            current_user.is_teacher or current_user.is_admin
        ):
            flask.abort(403)


api = Api(api_blueprint)
api.add_resource(GroupList, "/groups/")
api.add_resource(UserSelectList, "/users/select/")
api.add_resource(BasisList, "/basis/")
api.add_resource(CriteriaList, "/criterias/")
api.add_resource(TransactionList, "/transactions/")
api.add_resource(UserList, "/users/")
api.add_resource(AchievementList, "/achievements/", "/achievements/<status>")
api.add_resource(GiftList, "/gifts/")
api.add_resource(OrderList, "/orders/")
api.add_resource(NewsList, "/news/")
