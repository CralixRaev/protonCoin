from flask import url_for
from flask_restful import fields
from protonCoin.db.database import db


class News(db.Model):
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True
    )
    title = db.Column(db.String(255))
    description = db.Column(db.Text())

    @property
    def detail_url(self) -> str:
        return url_for("landing.news.detail", news_id=self.id)

    def __str__(self) -> str:
        return self.title

    @staticmethod
    def __json__() -> dict:
        _json = {
            "id": fields.Integer(),
            "title": fields.String(),
            "description": fields.String(),
        }
        return _json


class NewsQuery:
    @staticmethod
    def total_count() -> int:
        return News.query.count()

    @staticmethod
    def get_api(
        start: int = 0, length: int = 10, search: str | None = None, order_expr=None
    ) -> (int, list[News]):
        news_query = News.query
        count = news_query.count()
        if search:
            news_query = news_query.filter(News.title.ilike(f"%{search}%"))
            count = news_query.count()
        if order_expr is not None:
            news_query = news_query.order_by(*order_expr)
        news_query = news_query.limit(length).offset(start)
        return count, news_query.all()

    @staticmethod
    def get_all_news() -> list[News]:
        return News.query.all()

    @staticmethod
    def get_last_three() -> list[News]:
        return News.query.order_by(News.id.desc()).limit(3).all()

    @staticmethod
    def create_news(title, description) -> News:
        news = News()
        news.title = title
        news.description = description
        db.session.add(news)
        db.session.commit()
        return news

    @staticmethod
    def get_news_by_id(news_id: int):
        return db.get_or_404(News, news_id)

    @staticmethod
    def update_news(news_item, title, description):
        news_item.title = title
        news_item.description = description
        db.session.commit()
