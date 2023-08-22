import json
import numpy
from json import JSONEncoder
from flask import make_response
from werkzeug.exceptions import abort

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def response_body(status=None, query=None, data=None):
    return dict(status=status, query=query, data=data)

DEFAULT_RESPONSE = response_body(200, None, None)

def resp(res_detail=None):
    if res_detail is None:
        res_detail = DEFAULT_RESPONSE
    response = make_response(json.dumps(res_detail, cls=NumpyArrayEncoder), res_detail['status'])
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'content-type,token,Authorization'
    abort(response)
