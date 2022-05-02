from flask import Blueprint, render_template
from flask_login import login_required

userside = Blueprint('userside', __name__, template_folder='templates', static_folder='static')


@userside.route("/")
def index():
    return render_template("userside/profile.html")


@userside.route("/profile/")
@login_required
def profile():
    return render_template("userside/profile.html")