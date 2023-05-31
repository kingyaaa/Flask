from flask import jsonify, request, session, render_template_string, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from ..model.auth_user import User


@auth.route('/test', methods=['GET'])
@login_required
def test():
    return jsonify({
        "message": "This is a test data for auth"    
    })

@auth.route('/', methods=['GET','POST'])
def hello():
    return 'Hello, Auth!'

"""
函数:   登录
返回值: 登录成功的用户信息路由或错误信息
"""
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({
                'code': 1011, 
                'msg': 'post请求必须提供username和password'
                })
        user = User(username)
        # 返回用户实例
        if user:
            if username == user.username and password == user.password:
                #session['is_login'] = True
                #session['login_username'] = username
                # 增加loginmanager管理，注册用户信息
                login_user(user=user)
                return redirect(url_for('auth.profile'))
        return jsonify({'code': 1012, 'msg': 'post请求提供的用户名或密码错误'})

    else:
        return render_template_string("""
        <form method="post" id='login_form'>
        用户名: <input type='text' id='username' name='username' placeholder="请输入用户名" required/><br/>
        密码: <input type='password' id='password' name='password' placeholder="请输入密码" required/><br/>
        <input id="submit" name="submit" type="submit"  value="登录"/>
        </form>
        """)

@auth.route('/profile', methods=['GET','POST'])
#@login_required
def profile():
    return current_user.username + "登录成功"

@auth.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    # 可以省略手动设置会话的步骤
    """
    session.pop('login_username',None)
    session['is_login'] = False
    session.clear()
    """
    logout_user()
    return redirect(url_for('auth.login'))