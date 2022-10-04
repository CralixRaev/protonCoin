import logging
import os
from typing import Any

import click
from dotenv import load_dotenv
from flask import Flask, abort, send_from_directory, Blueprint
from flask_login import LoginManager, login_required
from flask_migrate import Migrate
from flask_uploads import configure_uploads, UploadSet

from blueprints.admin.admin import admin
from blueprints.api.api import api_blueprint as api
from blueprints.landing.landing import landing
from blueprints.login.login import login
from blueprints.teacher.teacher import teacher
from db.database import db
from db.models.balances import BalanceQuery
from db.models.user import User, UserQuery
from uploads import avatars, gift_images, achievement_files
from util import admin_required

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_STRING") or \
                                        'sqlite:///test.db?check_same_thread=False'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['COIN_UNIT'] = "ПРОтоКоин"
app.config['UPLOADS_DEFAULT_DEST'] = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                  'uploads')
app.config['UPLOADS_AUTOSERVE'] = False

_uploads = Blueprint("_uploads", "_uploads")


# require admin for all not-proxied uploads
@_uploads.route('/<setname>/<path:filename>')
@login_required
@admin_required
def uploaded_file(setname: UploadSet, filename: str) -> Any:
    config = app.upload_set_config.get(setname)  # type: ignore
    if config is None:
        abort(404)
    return send_from_directory(config.destination, filename)


app.register_blueprint(_uploads, url_prefix="/uploads")
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(teacher, url_prefix='/teacher')
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
migrate = Migrate(app, db, render_as_batch=True, compare_type=True)

configure_uploads(app, avatars)
configure_uploads(app, gift_images)
configure_uploads(app, achievement_files)

# log only in production mode.
if not app.debug:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.ERROR)
    app.logger.addHandler(stream_handler)


def main():
    with app.app_context():
        # ensure what default "bank" balance is present
        BalanceQuery.ensure_bank_balance()
    app.run(debug=True, host='0.0.0.0', port=80)


if __name__ == "__main__":
    main()
