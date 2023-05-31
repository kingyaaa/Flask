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

class User(object):
    """
    用户类
    """
    def __init__(self, username='null'):
        if username not in user_dict.keys():
            username = 'null'
        data = user_dict.get(username)
        self.id = data.get('id')
        self.username = data.get('username')
        self.password = data.get('password')
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
        return '<User %r>' % self.username

    """
    函数： query
    参数： 用户名
    使用： 在加载用户时调用，返回用户实例/None
    """
    @staticmethod
    def query(username):
        if username is None: username = 'null'
        return User(username)

    def get_id(self):
        return str(self.username)
