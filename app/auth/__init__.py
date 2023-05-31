from flask import Blueprint
from flask_login import LoginManager

auth = Blueprint('auth', __name__)

from . import views

lm = LoginManager()
lm.session_protection = 'strong'
lm.login_view = 'auth.login'
