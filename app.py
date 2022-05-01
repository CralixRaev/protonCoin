import os
from flask import Flask
from blueprints.admin.admin import admin
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

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(login, url_prefix='/login')

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def main():
    db.init_app(app)
    from db import __all_models

    with app.app_context():
        db.drop_all()
        db.create_all()

    app.run(debug=True, host='127.0.0.1', port=5001)


if __name__ == "__main__":
    main()
