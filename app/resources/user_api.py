from typing_extensions import Required
from xml.dom import ValidationErr
from flask_restful import Resource, reqparse
from app.libs.error import APIException

from app.libs.error_code import ParameterException
from ..auth.forms import UserForm, RegisterUserForm
from flask import jsonify
from wtforms.validators import ValidationError

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
        
        return {'message': 'User registration'}

class UserLogin(Resource):
    def post(self):
        data = user_parser.parse_args()
        # 表单验证，在form.validate中检查用户和密码
        try:
            form = UserForm().validate_for_api()
        except ValidationError as e:
            return jsonify({
                'status': 'error',
                'message': "User not existed"
            })
        # 获取数据库中的用户信息
        #user = form.get_user()
        return jsonify({
            'status': 'success',
            'message': 'user login'
        })
        

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

class TokenRefresh(Resource):
    def post(self):
        return {'message': 'Token refresh'}
