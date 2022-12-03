import io
from tempfile import NamedTemporaryFile

import flask
import openpyxl
from flask import redirect, render_template, url_for, request, Response, Blueprint
from flask_login import login_required
from openpyxl.utils import get_column_letter
from openpyxl.workbook import Workbook
from openpyxl.worksheet.dimensions import DimensionHolder, ColumnDimension
from werkzeug.datastructures import MultiDict

from blueprints.manage.admin.users.forms.import_user import UserImportForm
from blueprints.manage.admin.users.forms.user import UserForm
from db.models.group import GroupQuery
from db.models.user import UserQuery
from util import admin_required, redirect_to_back

user_methods = Blueprint('user_methods', __name__)


@user_methods.route('/delete/')
@admin_required
def delete_user():
    user_id = request.args.get("id")
    user = UserQuery.get_user_by_id(user_id)
    UserQuery.delete_user(user)
    flask.flash(f"Пользователь ID: {user.id} - {user.full_name} успешно удалён", "success")
    return redirect_to_back()


@user_methods.route('/new_password/', methods=['GET', 'POST'])
def new_password():
    password = UserQuery.new_password(request.args.get('id'))
    flask.flash(f"Новый пароль для пользователя: {password}", "success")
    return redirect_to_back()
