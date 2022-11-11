import json
import logging
import os
import uuid
from dataclasses import dataclass
from typing import Any, Mapping

import click
from dotenv import load_dotenv
from flask import Flask, abort, send_from_directory, Blueprint, url_for, current_app, redirect
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user
from flask_migrate import Migrate
from flask_saml2.sp import ServiceProvider
from flask_saml2.sp.views import SAML2View
from flask_saml2.utils import certificate_from_file, private_key_from_file
from flask_uploads import configure_uploads, UploadSet

from blueprints.admin.admin import admin
from blueprints.api.api import api_blueprint as api
from blueprints.landing.landing import landing
# from blueprints.login.login import login
from blueprints.teacher.teacher import teacher
from db.database import db
from db.models.balances import BalanceQuery
from db.models.group import GroupQuery
from db.models.user import User, UserQuery
from util import admin_required
from uploads import gift_images, achievement_files
from flask_redis import Redis

SP_CERTIFICATE = certificate_from_file("sp_certificate.pem")
SP_PRIVATE_KEY = private_key_from_file("sp_private-key.pem")
IDP_CERTIFICATE = certificate_from_file("idp_certificate.pem")

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_STRING") or \
                                        'sqlite:///test.db?check_same_thread=False'
app.config['SAML2_SP'] = {
    'certificate': SP_CERTIFICATE,
    'private_key': SP_PRIVATE_KEY,
}
app.config['SERVER_NAME'] = 'localhost'
app.config['SAML2_IDENTITY_PROVIDERS'] = [
    {
        'CLASS': 'flask_saml2.sp.idphandler.IdPHandler',
        'OPTIONS': {
            'display_name': 'ProtonSAML_IDP',
            'entity_id': 'http://localhost:9000/saml/metadata.xml',
            'sso_url': 'http://localhost:9000/saml/login/',
            'slo_url': 'http://localhost:9000/saml/logout/',
            'certificate': IDP_CERTIFICATE,
        },
    },
]
app.config['SAML_IDP_BASE_URL'] = "http://localhost:9000/"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['COIN_UNIT'] = "ПРОтоКоин"
app.config['UPLOADS_DEFAULT_DEST'] = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                  'uploads')
app.config['UPLOADS_AUTOSERVE'] = False
app.config['REDIS_HOST'] = "localhost"
app.config['REDIS_PORT'] = "6379"

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


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login.login"
login_manager.login_message = "Пожалуйста, войдите, что бы получить доступ к этой странице"

redis_client = Redis(app)


class Manage(SAML2View):
    def get(self):
        return redirect(current_app.config[
                            "SAML_IDP_BASE_URL"] +
                        f"manage/?next={self.sp.get_account_manage_return_url()}")


class ProtonServiceProvider(ServiceProvider):
    blueprint_name = "login"

    def get_logout_return_url(self):
        return url_for('landing.index', _external=True)

    def get_default_login_return_url(self):
        return url_for('landing.index', _external=True)

    def login_successful(self, auth_data, relay_state):
        attributes = auth_data.attributes
        print(attributes)
        user = UserQuery.create_or_update(attributes)
        GroupQuery.create_or_update(attributes)
        login_user(user, remember=True)
        return super().login_successful(auth_data, relay_state)

    def get_account_manage_return_url(self) -> str:
        return url_for('landing.index', _external=True)


sp = ProtonServiceProvider()


@login_manager.user_loader
def load_user(user_id):
    return UserQuery.get_user_by_id(user_id)



db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True, compare_type=True)

configure_uploads(app, gift_images)
configure_uploads(app, achievement_files)

# log only in production mode.
if not app.debug:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.ERROR)
    app.logger.addHandler(stream_handler)

app.register_blueprint(_uploads, url_prefix="/uploads")
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(teacher, url_prefix='/teacher')
# app.register_blueprint(login, url_prefix='/login')
app.register_blueprint(landing, url_prefix='/')
# app.register_blueprint(api, url_prefix='/api/v1/')
sp_bp = sp.create_blueprint()
sp_bp.add_url_rule("/manage/", view_func=Manage.as_view('manage', sp=sp))
app.register_blueprint(sp_bp, url_prefix='/saml/')


def main():
    with app.app_context():
        # ensure what default "bank" balance is present
        BalanceQuery.ensure_bank_balance()
    app.run(debug=True, host='0.0.0.0', port=80)


if __name__ == "__main__":
    main()
