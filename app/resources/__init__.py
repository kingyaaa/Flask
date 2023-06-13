from flask_restful import Api
from .user_api import *
api = Api()

def init_api(app):
    api.init_app(app)

api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin,'/login')
api.add_resource(AllUsers,'/users')
api.add_resource(TokenRefresh,'/token/refresh')
