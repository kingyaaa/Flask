"""
* 实现基础配置及测试类（和生产类）配置
"""
import logging
import datetime
import os

class BaseConfig(object):
    # 安全和session
    SECRET_KEY = os.environ.get('APP_SECRET_KEY') or "miyao=1234567890"  # flask app运行要用到的秘钥
    SESSION_TYPE = 'null'
    SESSION_KEY_PREFIX = "session:"
    SESSION_PERMANENT = False
    CSRF_ENABLED = True
    REMEMBER_COOKIE_DURATION = datetime.timedelta(days=3)
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=3)
    APP_SALT = os.environ.get('APP_SALT') or 'secure_key'
    WTF_CSRF_SECRET_KEY = SECRET_KEY
    JSON_AS_ASCII = False
    # 定义静态目录的位置
    BASE_PATH = os.path.abspath(os.path.dirname(__file__))
    # ...
    # 静态文件压缩相关
    # ...
    # 绑定信息
    APP_NAME = 'flask_auth'
    APP_HOST = '0.0.0.0'  # app 运行绑定的ip
    APP_PORT = 5001  # app 运行绑定的端口
    APP_DEBUG = True  # 开启debug模式
    APP_THREADED = True  # 启用多线程模式
    LOG_LEVEL = logging.INFO
    LOG_PATH = os.path.join(os.path.dirname(BASE_PATH), 'logs/')
    PID_PATH = os.path.join(BASE_PATH + "{}_{}.pid".format(APP_NAME, APP_PORT))
    LOG_NAME = "{}_{}.log".format(APP_NAME, APP_PORT)

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mypassword@localhost:3306/flask_auth'

    @staticmethod
    def init_app(app):
        pass

class TestConfig(BaseConfig):
    """
    测试环境 默认
    """
    APP_NAME = 'flask_auth_test'
    APP_HOST = '127.0.0.1'
    APP_PORT = 5001
    PID_PATH = os.path.join(BaseConfig.BASE_PATH + "{}_{}.pid".format(APP_NAME, APP_PORT))
    LOG_NAME = "{}_{}_test.log".format(APP_NAME, APP_PORT)

class ProductionConfig(BaseConfig):
    """
    线上环境
    """
    APP_NAME = 'flask_auth'
    APP_HOST = '0.0.0.0'
    APP_PORT = 5000
    PID_PATH = os.path.join(BaseConfig.BASE_PATH + "{}_{}.pid".format(APP_NAME, APP_PORT))
    LOG_NAME = "{}_{}.log".format(APP_NAME, APP_PORT)

config = {
    'test': TestConfig,
    'production': ProductionConfig,
    'default': TestConfig
}