import os

import click
from flask import Flask
from flask_migrate import Migrate
from flask_uploads import UploadSet, IMAGES, configure_uploads

from blueprints.admin.admin import admin
from blueprints.api.api import api_blueprint as api
from blueprints.landing.catalog.catalog import catalog
from blueprints.landing.landing import landing
from blueprints.login.login import login
from db.database import db
from flask_login import LoginManager
from dotenv import load_dotenv

from db.models.balances import BalanceQuery
from db.models.user import User, UserQuery
from uploads import avatars, gift_images

load_dotenv()

app = Flask(__name__)

# TODO: use postgresql DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db?check_same_thread=False'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['COIN_UNIT'] = "ПРОтоКоин"
app.config['UPLOADS_DEFAULT_DEST'] = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                  'uploads')
app.config['UPLOADS_AUTOSERVE'] = True

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(login, url_prefix='/login')
app.register_blueprint(landing, url_prefix='/')
app.register_blueprint(api, url_prefix='/api/v1/')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login.index"
login_manager.login_message = "Пожалуйста, войдите, что бы получить доступ к этой странице"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


from db.__all_models import *


@app.cli.command("create_admin")
@click.argument("name")
@click.argument("surname")
@click.argument("patronymic")
def create_admin(name, surname, patronymic):
    user_object, password = UserQuery.create_user(name, surname, patronymic, is_admin=True)

    click.echo(f"Админ создан. Логин: {user_object.login}, пароль: {password}")


@app.cli.command("reset_password")
@click.argument("login")
def create_admin(login):
    password = UserQuery.new_password(UserQuery.get_user_by_login(login).id)

    click.echo(f"Пароль изменён. Новый пароль: {password}")


db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)

configure_uploads(app, avatars)
configure_uploads(app, gift_images)


def main():
    with app.app_context():
        # ensure what default "bank" balance is present
        BalanceQuery.ensure_bank_balance()
    app.run(debug=True, host='0.0.0.0', port=80)


if __name__ == "__main__":
    main()
