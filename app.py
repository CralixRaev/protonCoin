import os
from flask import Flask, redirect, url_for
from flask_migrate import Migrate

from blueprints.admin.admin import admin
from blueprints.landing.landing import landing
from blueprints.login.login import login
from db.database import db
from flask_login import LoginManager
from dotenv import load_dotenv

from db.models.user import User

load_dotenv()

app = Flask(__name__)

# TODO: use postgresql DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db?check_same_thread=False'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['COIN_UNIT'] = "ПротоКоин"

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(login, url_prefix='/login')
app.register_blueprint(landing, url_prefix='/')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login.index"
login_manager.login_message = "Пожалуйста, войдите, что бы получить доступ к этой странице"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


db.init_app(app)
migrate = Migrate(app, db)
from db import __all_models


def main():
    app.run(debug=True, host='127.0.0.1', port=5001)


if __name__ == "__main__":
    main()
