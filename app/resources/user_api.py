from typing_extensions import Required
from xml.dom import ValidationErr
from flask_restful import Resource, reqparse
from app.libs.error import APIException

from app.libs.error_code import ParameterException
from ..auth.forms import UserForm, RegisterUserForm
from flask import jsonify
from wtforms.validators import ValidationError
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt)

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', help='Username cannot be None', required=True)
user_parser.add_argument('password', help='Password cannot be None', required=True)

class UserRegistration(Resource):
    def post(self):
        data = user_parser.parse_args()
        #检查输入的字符串格式
        #检查username是否已存在
        form = RegisterUserForm().validate_for_api()
        from ..model.auth_user import User
        user = User().add_user(form)
        #access_token = create_access_token(identity=data['username'])
        #refresh_token = create_refresh_token(identity=data['username'])
        # 注册之后转到登录界面，登录成功之后再分发token
        return {
            'message': 'User registration'
            #'access_token': access_token,
            #'refresh_token': refresh_token
        }

class UserLogin(Resource):
    def post(self):
        data = user_parser.parse_args()
        # 表单验证，在form.validate中检查用户和密码
        form = UserForm().validate_for_api()
        # 获取数据库中的用户信息
        #user = form.get_user()
        access_token = create_access_token(identity=data['username'])
        refresh_token = create_refresh_token(identity=data['username'])
        return {
            'message': 'User login',
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        

class AllUsers(Resource):
    '''
    获取已注册用户列表(only for test)
    '''
    def get(self):
        from ..model.auth_user import User
        return User.query_all()
        #return {'message': 'List of users'}

    def delete(self):
        return {'message': 'Delete all users'}


# 用refresh_token来刷新access_token
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'message': 'Token refresh'}

class TestAPI(Resource):
    def get(self):
        return {'message': 'test for docker deploy...'}