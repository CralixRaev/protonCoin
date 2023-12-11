import os
from datetime import timedelta


class Config:
    COIN_UNIT = "ПРОтоКоин"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PASSWORD_RESET_EXPIRE = timedelta(hours=1)
    UPLOADS_DEFAULT_DEST = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "uploads"
    )
    UPLOADS_AUTOSERVE = False
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://login:password@localhost/protoncoin"
    )
    SECRET_KEY = None
    SMARTCAPTCHA_SERVER_KEY = None
    SMARTCAPTCHA_CLIENT_KEY = None
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    MAIL_SERVER = None
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
