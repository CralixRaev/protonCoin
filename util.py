import re
import secrets
import threading
from functools import wraps
from io import BytesIO
from urllib.parse import urlparse, urljoin

import flask
from PIL import Image
from flask import request, redirect, copy_current_request_context, current_app
from flask_login import current_user
from flask_uploads import UploadSet
from transliterate import translit
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from uploads import avatars

MAX_PASSWORD_LENGTH = 8


def convert_to_webp(file: FileStorage, processing=None) -> FileStorage:
    im = Image.open(file.stream)
    if processing:
        processing(im)
    stream = BytesIO()
    im.save(stream, "webp")
    stream.seek(0)
    file.stream = stream
    filename_split = file.filename.split(".")
    filename_split[-1] = "webp"
    file.filename = ".".join(filename_split)
    return file


def save_upload(file: FileStorage, upload_set: UploadSet, processing=None) -> str:
    file.filename = secure_filename(translit(file.filename, "ru", True))
    return upload_set.save(convert_to_webp(file, processing))


def upload_avatar(file: FileStorage, size: tuple[int, int] = (512, 512)) -> str:
    def avatar_processing(image):
        image.thumbnail(size)

    return save_upload(file, avatars, processing=avatar_processing)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in {"http", "https"} and ref_url.netloc == test_url.netloc


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:
            return flask.abort(403)
        return func(*args, **kwargs)

    return decorated_view


def teacher_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_teacher:
            return flask.abort(403)
        return func(*args, **kwargs)

    return decorated_view


def teacher_or_admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not (current_user.is_teacher or current_user.is_admin):
            return flask.abort(403)
        return func(*args, **kwargs)

    return decorated_view


def password_check(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    length_error = len(password) <= MAX_PASSWORD_LENGTH

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # overall result
    password_ok = not (
        length_error or digit_error or uppercase_error or lowercase_error
    )
    return {
        "password_ok": password_ok,
        "length_error": length_error,
        "digit_error": digit_error,
        "uppercase_error": uppercase_error,
        "lowercase_error": lowercase_error,
    }


ALPHABET = [
    "a",
    "e",
    "f",
    "g",
    "h",
    "m",
    "n",
    "t",
    "y",
    "A",
    "B",
    "E",
    "F",
    "G",
    "H",
    "J",
    "K",
    "L",
    "M",
    "N",
    "Q",
    "R",
    "T",
    "X",
    "Y",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
]


def random_password():
    password = "".join(secrets.choice(ALPHABET) for _ in range(8))
    while password_check(password)["password_ok"]:
        password = "".join(secrets.choice(ALPHABET) for _ in range(8))
    return password


class ABCQuery:
    Model = None
    Search_expr = None

    def __init__(self):
        func = list_get_factory(self.Model, self.Search_expr)
        setattr(self, func.__name__, func)


def list_get_factory(model, search_expr):
    def _get_model(
        start: int = 0, length: int = 10, search: str | None = None, order_expr=None
    ) -> (int, list[model]):
        model_query = model.query
        count = model_query.count()
        if search:
            model_query = model_query.filter(search_expr.ilike(f"%{search}%"))
            count = model_query.count()
        if order_expr is not None:
            model_query = model_query.order_by(*order_expr)
        model_query = model_query.limit(length).offset(start)
        return count, model_query.all()

    _get_model.__name__ = "get_api"
    return _get_model


def redirect_to_back():
    back = request.args.get("back", None)
    if is_safe_url(back):
        return redirect(back)
    else:
        flask.abort(400)


def is_teacher_to_bool() -> bool:
    return request.args.get("is_teacher", "false") == "true"


def send_email_async(message):
    @copy_current_request_context
    def send_message(message):
        current_app.extensions["mail"].send(message)

    sender = threading.Thread(name="mail_sender", target=send_message, args=(message,))
    sender.start()
