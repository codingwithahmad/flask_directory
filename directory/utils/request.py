from functools import wraps
from flask import request


def json_only(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        if not request.is_json:
            return {'error': 'JSON Only!'}, 400
        return fn(*args, **kwargs)
    return decorator
