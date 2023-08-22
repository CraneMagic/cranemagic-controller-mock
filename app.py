from flask import Flask, make_response, request
from flask_cors import *

import logging
import time

from dotenv import load_dotenv

load_dotenv('./.env')

app = Flask(__name__)
app.config.from_pyfile('config.py')

# from auth import auth_bp
# from yourBlueprint import yourBlueprint_bp

# app.register_blueprint(auth_bp, url_prefix='/auth')
# app.register_blueprint(yourBlueprint_bp, url_prefix='/yourBlueprint')

CORS(app, support_credentials=True)

@app.before_request
def before_request():
	print("[%s][%s][%s]" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), request.method, request.full_path))
	reqJson = request.get_json(silent=True)
	print(str(reqJson))

@app.after_request
def after_request(resp):
	resp = make_response(resp)
	resp.headers['Access-Control-Allow-Origin'] = '*'
	resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
	resp.headers['Access-Control-Allow-Headers'] = 'content-type,token,Authorization'
	return resp

# app.after_request(after_request)

@app.route('/')
def home():
    # error(LOGIN_FAILED)
	return 'Hello Flask With Blueprint'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)