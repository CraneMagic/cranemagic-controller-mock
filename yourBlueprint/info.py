from flask import current_app, request
from yourBlueprint import before, yourBlueprint_bp

from utils._resp import resp, response_body
from utils._error import err_resp

import os
env = os.environ

@yourBlueprint_bp.route('/YourUrl', methods=["GET", "POST"])
@before
def your_url(*args, **kwargs):
    print(*args)
    resp(response_body(200, "YourUrl", {}))