from flask import Blueprint, redirect, url_for
from flask_login import login_required

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


@admin.route('/')
@login_required
def index():
    return '!'

