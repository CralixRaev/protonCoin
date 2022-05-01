from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_user

from blueprints.login.forms.login import LoginForm
from db.models.user import UserQuery

login = Blueprint('login', __name__, template_folder='templates', static_folder='static')


@login.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    context = {
        'form': form,
        'title': 'Авторизация'
    }
    if form.validate_on_submit():
        user = UserQuery.get_user_by_login(form.login.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login/login.html', message="Неправильный логин или пароль",
                               **context)
    return render_template("login/login.html", **context)
