from flask import Blueprint
yourBlueprint_bp = Blueprint('yourBlueprint', __name__)
from functools import wraps

def before(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        something = None

        return f(something, *args, **kwargs)
    return decorator


from yourBlueprint.info import *
from yourBlueprint.op import *