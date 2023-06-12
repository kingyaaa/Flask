from flask_restful import Api
from .user_api import *
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt)
api = Api()

def init_api(app):
    api.init_app(app)

api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin,'/login')
api.add_resource(AllUsers,'/users')
api.add_resource(TokenRefresh,'/token/refresh')
