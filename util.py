import re
from functools import wraps
from urllib.parse import urlparse, urljoin

import flask
from flask import request
from flask_login import current_user
from flask_uploads import UploadSet
from transliterate import translit
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


def save_upload(file: FileStorage, upload_set: UploadSet) -> str:
    file.filename = secure_filename(translit(file.filename, 'ru', True))
    return upload_set.save(file)


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
