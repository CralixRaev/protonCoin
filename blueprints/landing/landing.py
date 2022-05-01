from flask import Blueprint

landing = Blueprint('landing', __name__, template_folder='templates', static_folder='static')


@landing.route("/")
def index():
    return "i am a beautiful page!"

