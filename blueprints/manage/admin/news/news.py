import flask
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from werkzeug.datastructures import MultiDict

from blueprints.manage.admin.news.forms.news import NewsForm
from db.models.news import NewsQuery
from util import admin_required

news = Blueprint("news", __name__, template_folder="templates", static_folder="static")


@news.route("/")
@login_required
@admin_required
def index():
    context = {
        "title": "Новости",
    }
    return render_template("news/news.html", **context)


@news.route("/create/", methods=["GET", "POST"])
@login_required
@admin_required
def create_news():
    form = NewsForm()
    context = {"title": "Создать новость", "form": form}
    if form.validate_on_submit():
        NewsQuery.create_news(form.title.data, form.description.data)
        flask.flash("Новость успешно создана.", "success")
        return redirect(url_for("manage.admin.news.index"))
    return render_template("news/news_edit.html", **context)


@news.route("/edit/", methods=["GET", "POST"])
@login_required
@admin_required
def edit_news():
    news_item = NewsQuery.get_news_by_id(int(request.args.get("news_id")))
    form = NewsForm()
    context = {"title": "Редактировать новость", "form": form}
    if form.validate_on_submit():
        NewsQuery.update_news(news_item, form.title.data, form.description.data)
        flask.flash("Новость успешно обновлена.", "success")
        return redirect(url_for("manage.admin.news.index"))
    model_data = MultiDict(news_item.__dict__.items())
    form = NewsForm(model_data)
    context["form"] = form
    return render_template("news/news_edit.html", **context)
