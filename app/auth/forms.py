from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, Regexp, EqualTo, InputRequired, Length, email_validator
from flask import request

from app.libs.error import APIException
from ..libs.error_code import ParameterException

class BaseForm(Form):
    def __init__(self):
        data = request.get_json()
        args = request.args.to_dict()
        super(BaseForm, self).__init__(data=data, **args)
    
    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            raise ParameterException(msg=self.errors)
        return self

class RegisterUserForm(BaseForm):
    """
    注册表单
    validators: 验证器,不会直接抛出异常,而是将错误信息放入form.error中
    render_kw: 渲染属性
    """
    '''
    username = StringField(label="登录账号", validators=[DataRequired('请输入登录账号'), Length(8,64),
                                                      Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名只能使用字符串、数字和*%等特殊字符')])
    #real_name = StringField(label="真实姓名", validators=[DataRequired('请输入姓名')])
    #email = StringField(label="邮箱", validators=[DataRequired('请输入邮箱'), Email('邮箱格式不正确')])
    password = PasswordField(label="密码", validators=[InputRequired()])
    #前端验证
    '''
    username = StringField('Username', validators=[Length(8,64)])
    password = PasswordField('Password', validators=[Length(8,16)])
    

class UserForm(BaseForm):
    username = StringField('Username', validators=[Length(max=64)])
    password = PasswordField('Password', validators=[Length(8,16)])
        
    def get_user(self):
        from ..model.auth_user import User
        user = User.query.filter(User.name == self.username.data).first()
        return user
    
    def validate_username(self, field):
        #return self.get_user()
        if not self.get_user():
            raise ValidationError('Invalid username!')
                

    def validate_password(self, field):
        if not self.get_user():
            return 
        if not self.get_user().check_password(field.data):
            raise ValidationError('Incorrect password!')