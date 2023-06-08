from operator import truediv
from flask_login import UserMixin
from sqlalchemy import Table
from app import database_connection_info, db
from passlib.hash import pbkdf2_sha256 as sha256
import hashlib
connection_session, db_model, engine_metadata = database_connection_info()
"""
# 定义一个字典，存储用户的用户名和密码信息
user_dict = {
    'null': {},
    'admin': {
        'id': 1,
        'username': 'admin',
        'password': 'admin'
    },
    'test': {
        'id': 2,
        'username': 'test',
        'password': 'password'
    }
}
"""
class User(db.Model, UserMixin):
    """
    用户类
    """
    __table__ = Table('user', engine_metadata, autoload_with=db.engine)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __repr__(self):
        return '<User %r>' % self.name

    def get_id(self):
        return str(self.name)
    
    def get_password(self):
        return self.password
    
    def check_password(self, password):
        # if password == str(self.password):
        if User.verify_hash(password, self.password):
            return password
        return None

    #实例方法,地一个
    def add_user(self, register_form):
        """
        新增用户
        param: register_form: 注册表单数据
        return: 用户实例
        """
        user = User(
            name=register_form.username.data,
            #password=register_form.password.data,
            password=User.generate_hash(register_form.password.data)
            #real_name=register_form.real_name.data,
            #email=register_form.email.data
        )
        connection_session.add(user)
        connection_session.commit()
        return user

    #类方法装饰器,不用实例化对象就能使用
    #参数: cls(类，访问类的属性和其他类方法)
    @classmethod
    def query_all(cls):
        def to_json(x):
            return {
            'username': x.name,
            'password': x.password
            }
        return {'users': list(map(lambda x: to_json(x), User.query.all()))}

    #hashlib.sha256是一种加密方式，也可以选择其他的、更好的方式
    @staticmethod
    def generate_hash(password):
        #return sha256.hash(password)
        # 将密码编码为 UTF-8 字节串
        password_bytes = password.encode('utf-8')
        
        # 使用 SHA-256 哈希函数计算密码的哈希值
        hashed_password = hashlib.sha256(password_bytes).hexdigest()

        #print('generate_hash')
        #print("password_bytes:", password_bytes)
        #print("hashed_password:", hashed_password)
        return hashed_password

    @staticmethod
    def verify_hash(password, hashed_password):
        # 将密码编码为 UTF-8 字节串
        #print(password)
        password_bytes = password.encode('utf-8')
        # 使用 SHA-256 哈希函数计算输入密码的哈希值
        input_hash = hashlib.sha256(password_bytes).hexdigest()
        #print('verify_hash:')
        #print("password_bytes:", password_bytes)
        #print("input_hash", input_hash)
        #print("hashed_password:", hashed_password)

        # 比较输入密码的哈希值与存储的哈希值是否相同
        if input_hash == hashed_password:
            return True
        else:
            return False

