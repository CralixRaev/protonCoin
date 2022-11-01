import re
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

def convert_to_webp(file: FileStorage, processing = None) -> FileStorage:
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


def save_upload(file: FileStorage, upload_set: UploadSet, processing = None) -> str:
    file.filename = secure_filename(translit(file.filename, 'ru', True))
    return upload_set.save(convert_to_webp(file, processing))


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

