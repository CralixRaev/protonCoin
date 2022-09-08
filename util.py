from functools import wraps
from urllib.parse import urlparse, urljoin

import flask
from flask import request
from flask_login import current_user


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
