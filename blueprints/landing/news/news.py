from flask import Blueprint, render_template

from db.models.news import NewsQuery

news = Blueprint("news", __name__, template_folder="templates", static_folder="static")


@news.route("/<int:news_id>/")
def detail(news_id: int = 0):
    news = NewsQuery.get_news_by_id(news_id)
    context = {"title": news.title, "news": news}
    return render_template("news/detail.html", **context)
