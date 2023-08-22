from flask import Blueprint
auth_bp = Blueprint('auth', __name__)
from functools import wraps

def before(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        something = None

        return f(something, *args, **kwargs)
    return decorator


from auth.info import *
from auth.op import *