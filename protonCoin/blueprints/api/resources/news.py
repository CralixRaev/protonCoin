from flask import request
from flask_restful import Resource

from protonCoin.blueprints.api.utils import ListQuery, generate_list_response
from protonCoin.db.models.news import News, NewsQuery


class NewsList(Resource):
    def get(self) -> dict:
        args = ListQuery().load(request.args)
        rows = [None, (News.id,), (News.title,)]
        return generate_list_response(
            args, rows, NewsQuery.get_api, NewsQuery.total_count, News.__json__()
        )
