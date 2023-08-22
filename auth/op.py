from flask import current_app, request
from auth import auth_bp
# , token_required, full_authority_required
# from werkzeug.local import LocalProxy
# import logging

# logger = LocalProxy(lambda: current_app.logger)
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime, time
import re
import logging

# from .info import fetch_user_list_operation
from utils._database import query, mutate
from utils._resp import response_body, resp
from utils._error import err_resp, DATABASE_ERROR, UNKNOWN_ERROR, NOITEM_ERROR, TOKEN_INVAILD, LOGIN_FAILED, NO_CURRUSER, LOGIN_FAILED, EMPTY_INPUT, USERNAME_INVAILD, WRONG_USERID, WRONG_PHONE

import os
env = os.environ

def get_auth_list():
    return []

@auth_bp.route('/login', methods=['POST'])
def login():
    auth = request.authorization   
    if not auth or not auth.username or not auth.password:  
        print("[%s][%s][Login Failed]" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), request.full_path))
        err_resp(LOGIN_FAILED, request.path)
    all_users = get_auth_list()
    # print(all_users)
    if len([user for user in all_users if user.get('username') == auth.username]):
        user = [user for user in all_users if user.get('username') == auth.username][0]
        if check_password_hash(user.get('password'), auth.password):  
            # token = jwt.encode({'id': user.get('id'), 'iat' : datetime.datetime.now(tz=datetime.timezone.utc), 'exp' : datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=365)}, current_app.config['SECRET_KEY'])  
            token = jwt.encode({'id': user.get('id'), 'iat' : datetime.datetime.now(tz=datetime.timezone.utc)}, current_app.config['SECRET_KEY'])  
            print("[%s][%s]" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), request.full_path), user)
            resp(response_body(200, request.path, { 'token' : token, 'user': user }))
    else:
        print("[%s][%s][No Current User]" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), request.full_path), auth.username)
        err_resp(NO_CURRUSER, request.path)
    err_resp(LOGIN_FAILED, request.path)

def after_register():

    return (True, [])

@auth_bp.route('/register', methods=['POST'])
def register():  
    print("[%s][%s]" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), request.full_path))
    reqJson = request.get_json(silent=True)
    # TODO: Your User parses
    nickname, email, phone, gender, password, locale = reqJson.get('nickname', None), reqJson.get('email', None), reqJson.get('phone', None), reqJson.get('gender', 0), reqJson.get('password', None), reqJson.get('locale', 'zh-CN')
    # TODO: Your MUST parses
    if not all([nickname, email, password]):
        err_resp(EMPTY_INPUT, request.path)
    # if not (re.match('^[A-Za-z0-9]+$', username)):
    #     err_resp(USERNAME_INVAILD, request.path)
    hashed_password = generate_password_hash(password, method='sha256')
    sql = "INSERT INTO User(nickname, email, phone, gender, password, locale) "\
          "VALUES('%s', '%s', '%s', '%s', '%s', '%s');" % (nickname, email, phone, gender, hashed_password, locale)
    (status, mutateRes) = mutate(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), sql.replace("'None'", "NULL"))
    if status:
        (status, mutateRes) = after_register()
        resp(response_body(200, request.path, None))
    elif DATABASE_ERROR.get(mutateRes[0], None):
        err_resp(DATABASE_ERROR.get(mutateRes[0], None), request.path)
    else:
        err_resp(UNKNOWN_ERROR, request.path)


# @auth_bp.route('/resetPassword', methods=['POST'])
# def reset_password():  
#     print("[%s][%s]" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), request.full_path))
#     reqJson = request.get_json(silent=True)    
#     id, username, password, phone, email  = reqJson.get('id', None), reqJson.get('username', None), reqJson.get('password', None), reqJson.get('phone', None), reqJson.get('email', None)
#     if not all([id, username, password, phone]):
#         err_resp(EMPTY_INPUT, request.path)
#     if not (re.match('^[A-Za-z0-9]+$', username)):
#         err_resp(USERNAME_INVAILD, request.path)
#     hashed_password = generate_password_hash(password, method='sha256')
#     res_username = fetch_user_list_operation(["`username`='%s'" % username])
#     res_id = fetch_user_list_operation(["`id`='%s'" % id, "`username`='%s'" % username])
#     res_phone = fetch_user_list_operation(["`id`='%s'" % id, "`username`='%s'" % username, "`phone`='%s'" % phone])
#     if not len(res_username):
#         err_resp(NO_CURRUSER, request.path)
#     if not len(res_id):
#         err_resp(WRONG_USERID, request.path)
#     if not len(res_phone):
#         err_resp(WRONG_PHONE, request.path)
#     sql = "UPDATE user SET `password`='%s' "\
#           "WHERE `id`='%s' AND `username`='%s' AND `phone`='%s';" % (hashed_password, id, username, phone)
#     (status, mutateRes) = mutate(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), sql)
#     if status:
#         resp(response_body(200, request.path, None))
#     elif DATABASE_ERROR.get(mutateRes[0], None):
#         err_resp(DATABASE_ERROR.get(mutateRes[0], None), request.path)
#     else:
#         err_resp(UNKNOWN_ERROR, request.path)
