import re
import secrets
import string
from functools import wraps
from io import BytesIO
from urllib.parse import urlparse, urljoin

import flask
from PIL import Image
from flask import request
from flask_login import current_user
from flask_uploads import UploadSet
from transliterate import translit
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from uploads import avatars


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
    file.filename = secure_filename(translit(file.filename, 'ru', True))
    return upload_set.save(convert_to_webp(file, processing))


def upload_avatar(file: FileStorage, size: tuple[int, int] = (512, 512)) -> str:
    def avatar_processing(image):
        image.thumbnail(size)

    return save_upload(file, avatars, processing=avatar_processing)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


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
    length_error = len(password) <= 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # overall result
    password_ok = not (length_error or digit_error or uppercase_error or lowercase_error)

    return {
        'password_ok': password_ok,
        'length_error': length_error,
        'digit_error': digit_error,
        'uppercase_error': uppercase_error,
        'lowercase_error': lowercase_error,
    }


ALPHABET = ['a', 'e', 'f', 'g', 'h', 'm', 'n', 't', 'y'] + \
           ['A', 'B', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'Q', 'R', 'T', 'X', 'Y'] + \
           ['2', '3', '4', '5', '6', '7', '8', '9']


def random_password():
    password = ''.join(secrets.choice(ALPHABET) for _ in range(8))
    while not password_check(password):
        password = ''.join(secrets.choice(ALPHABET) for _ in range(8))
    return password
