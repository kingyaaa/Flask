"""
* 实现实例化Flask的工厂方法
"""
from flask import Flask, jsonify, make_response
from werkzeug.exceptions import HTTPException
from flask_compress import Compress
from .auth import lm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import QueuePool
from sqlalchemy.schema import MetaData
from sqlalchemy import exc
from flask_jwt_extended import JWTManager
from .resources import init_api

# from app.auth import auth

# db = SQLAlchemy(engine_options={"poolclass": QueuePool, 'pool_size': 200, 'max_overflow': 100, 'pool_recycle': 300})
db = SQLAlchemy()

def create_app(cfg):
    """
    *********
    参数：需要配置的参数类
    方法：配置参数类,设置压缩,实例化相应,返回Flask实例
    *********
    """
    # app = Flask(__name__, template_folder=cfg.TEMPLATES_PATH, static_url_path='/', static_folder=cfg.STATIC_PATH)
    app = Flask(__name__)
    app.config.from_object(cfg)

    # 初始化压缩
    Compress(app=app)

    # 实例化
    db.init_app(app)
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')
    # 实例化访问控制
    lm.init_app(app)
    # 初始化api资源
    init_api(app)
    jwt = JWTManager(app)
    # 初始化响应
    init_response(app)

    return app

def init_response(app):
    @app.after_request
    def add_security_headers(response):
        # 响应安全头设置
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Sec-Fetch-Dest'] = 'document'
        response.headers['Sec-Fetch-Mode'] = 'navigate'
        response.headers['Sec-Fetch-Site'] = 'same-site'
        response.headers['Upgrade-Insecure-Requests'] = '1'
        # If you want all HTTP converted to HTTPS
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        return response

    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        # 错误提示信息
        return jsonify({'status': 'error', 'message': exc.description, 'code': exc.code}), exc.code

    @app.errorhandler(404)
    def url_not_found(e):
        return make_response(jsonify({'code': 404, 'message': '请求的url不存在', 'status': 'error'}), 404)

    @app.errorhandler(405)
    def method_is_not_allowed(e):
        return make_response(jsonify({'code': 405, 'message': '请求的方法不存在', 'status': 'error'}), 405)

    @app.errorhandler(500)
    def method_is_not_allowed(e):
        return make_response(jsonify({'code': 500, 'message': '内部错误', 'status': 'error'}), 500)
    
    # Flask_login的回调函数
    @lm.user_loader
    def load_user(username):
        # 查询用户信息，绑定到上下文
        from app.model.auth_user import User
        #try:
        #user = User().query(username)
        #except exc.StatementError:
        #    user = User().query(username)
        try:
            user = User.query.filter(User.name == username).first()
        except exc.StatementError:
            user = User.query.filter(User.name == username).first()
        return user 

"""
* 和数据库链接的基础信息
"""
def database_connection_info():
    connection_session = db.session
    db_model = db.Model
    engine_metadata = MetaData()
    return connection_session, db_model, engine_metadata


