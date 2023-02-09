import flask
import requests
from flask import Blueprint, redirect, url_for, render_template, current_app, request
from flask_login import login_user, logout_user, login_required, current_user

from blueprints.login.forms.login import LoginForm
from db.models.user import UserQuery
from util import is_safe_url

login = Blueprint('login', __name__, template_folder='templates', static_folder='static')


def _check_captcha(token):
    answer = requests.get(
        "https://captcha-api.yandex.ru/validate",
        {
            "secret": current_app.config['SMARTCAPTCHA_SERVER_KEY'],
            "token": token,
            "ip": request.remote_addr
        },
        timeout=3
    )
    server_output = answer.json()
    if answer.status_code != 200:
        current_app.logger.error(
            f"Allowing access due to captcha error: code={answer.status_code}; message={server_output()}")
        return True
    return server_output['status'] == 'ok'


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
        if not _check_captcha(request.form.get("smart-token")):
            flask.flash("Вы не прошли капчу", "danger")
        else:
            user = UserQuery.get_user_by_login(form.login.data)
            print(user)
            if user and user.check_password(form.password.data):
                print('login')
                login_user(user, remember=form.remember_me.data)
                UserQuery.update_auth_time(user)
                flask.flash('Успешный вход', "success")
                next_path = flask.request.args.get('next')
                if is_safe_url(next_path):
                    return redirect(next_path or url_for("landing.index"))
                else:
                    flask.abort(400)
            else:
                flask.flash("Неправильный логин или пароль", "danger")
    return render_template("login/login.html", **context)


@login_required
@login.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for("login.index"))
