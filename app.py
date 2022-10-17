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
from db.models.group import GroupQuery
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

    click.echo(f"Пароль изменён. Новый пароль: {password}") @ app.cli.command("reset_password")


@app.cli.command("import_folders")
@click.argument("folder")
def import_folders(folder):
    from openpyxl.worksheet.dimensions import DimensionHolder
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.dimensions import ColumnDimension
    import openpyxl

    groups = os.listdir(os.path.join(folder, "for_import"))
    for group in groups:
        groupname = os.path.basename(group).split(".")[0]
        if groupname:
            print(groupname)
            stage, letter = groupname[0], groupname[1]
            wb_read = openpyxl.load_workbook(os.path.join(folder, "for_import", group),
                                             read_only=True, data_only=True)
            ws_read = wb_read.active
            wb_write = openpyxl.Workbook()
            ws_write = wb_write.active
            [ws_write.cell(1, i + 1, name) for i, name in enumerate(['ФИО', 'Логин', 'Пароль'])]
            for row in ws_read.iter_rows(min_row=2):
                full_name = row[0].value
                if full_name:
                    split_name = full_name.split()
                    surname, name, patronymic = split_name[0], split_name[1], ' '.join(
                        split_name[2:])
                    user, password = UserQuery.create_user(name, surname,
                                                           patronymic if patronymic else None,
                                                           None, False, False,
                                                           GroupQuery.get_group_by_stage_letter(
                                                               stage,
                                                               letter))
                    ws_write.append((user.full_name, user.login, password))
            dim_holder = DimensionHolder(worksheet=ws_write)

            for col in range(ws_write.min_column, ws_write.max_column + 1):
                dim_holder[get_column_letter(col)] = ColumnDimension(ws_write, min=col,
                                                                     max=col,
                                                                     width=20)
            ws_write.column_dimensions = dim_holder

            wb_write.save(os.path.join(folder, "imported", f"{groupname}-imported.xlsx"))
    click.echo("Ну, вроде импортировали!")


@app.cli.command("import_teachers")
@click.argument("file")
def import_teachers(file):
    from openpyxl.worksheet.dimensions import DimensionHolder
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.dimensions import ColumnDimension
    import openpyxl
    wb_read = openpyxl.load_workbook(file, read_only=True, data_only=True)
    ws_read = wb_read.active
    wb_write = openpyxl.Workbook()
    ws_write = wb_write.active
    [ws_write.cell(1, i + 1, name) for i, name in enumerate(['ФИО', 'Логин', 'Пароль'])]
    for row in ws_read.iter_rows(min_row=2):
        full_name = row[1].value
        if full_name:
            split_name = full_name.split()
            stage, letter = row[0].value[0], row[0].value[1]
            print(stage, letter)
            print(GroupQuery.get_group_by_stage_letter(stage,
                                                 letter))
            surname, name, patronymic = split_name[0], split_name[1], ' '.join(split_name[2:])
            user, password = UserQuery.create_user(name, surname,
                                                   patronymic if patronymic else None,
                                                   None, False, True,
                                                   GroupQuery.get_group_by_stage_letter(stage,
                                                                                        letter))
            ws_write.append((user.full_name, user.login, password))
    dim_holder = DimensionHolder(worksheet=ws_write)

    for col in range(ws_write.min_column, ws_write.max_column + 1):
        dim_holder[get_column_letter(col)] = ColumnDimension(ws_write, min=col,
                                                             max=col,
                                                             width=20)
    ws_write.column_dimensions = dim_holder

    wb_write.save("teachers.xlsx")
    click.echo("Ну, вроде импортировали!")


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
