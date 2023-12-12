from protonCoin.config import Config


class DebugConfig(Config):
    SQLALCHEMY_DATABASE_URI = None
    SECRET_KEY = "64e499b91a1ad2bb85b291578cda74c1fa65a10788412e310947368c50e62240"
    SMARTCAPTCHA_SERVER_KEY = "8gGwmsw67sibzarVhkPl66JvhkJtu4iy6f2Ibw0A"
    SMARTCAPTCHA_CLIENT_KEY = "8gGwmsw67sibzarVhkPl7BJtbK1pML7kjIENUY1e"
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
