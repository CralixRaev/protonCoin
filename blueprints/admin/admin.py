from flask import Blueprint, redirect, url_for

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


@admin.route('/')
def index():
    return redirect(url_for('.login'))


@admin.route('/login/')
def login():
    return 'Welcome to login page'
