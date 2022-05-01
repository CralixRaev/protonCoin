import flask
from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_user, logout_user, login_required, current_user

from blueprints.login.forms.login import LoginForm
from db.models.user import UserQuery
from util import is_safe_url

login = Blueprint('login', __name__, template_folder='templates', static_folder='static')


@login.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("landing.index"))
    form = LoginForm()
    context = {
        'form': form,
        'title': 'Авторизация'
    }
    if form.validate_on_submit():
        user = UserQuery.get_user_by_login(form.login.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flask.flash('Успешный вход')
            next_path = flask.request.args.get('next')
            if not is_safe_url(next_path):
                return flask.abort(400)
            return redirect(next_path or url_for("landing.index"))
        return render_template('login/login.html', login_message="Неправильный логин или пароль",
                               **context)
    return render_template("login/login.html", **context)


@login_required
@login.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for("login.index"))
