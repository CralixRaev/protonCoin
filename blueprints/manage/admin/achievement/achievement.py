from flask import Blueprint, render_template


achievement = Blueprint(
    "achievement", __name__, template_folder="templates", static_folder="static"
)


@achievement.route("/")
def index():
    context = {
        "title": "Достижения",
    }
    return render_template("achievement/list_achievement.html", **context)
