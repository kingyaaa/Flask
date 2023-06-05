from flask_login import UserMixin
from sqlalchemy import Table
from app import database_connection_info, db
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

    def add_user(self, register_form):
        """
        新增用户
        param: register_form: 注册表单数据
        return: 用户实例
        """
        user = User(
            name=register_form.username.data,
            password=register_form.password.data,
            real_name=register_form.real_name.data,
            email=register_form.email.data
        )
        connection_session.add(user)
        connection_session.commit()
        return user