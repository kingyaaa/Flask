from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, Regexp, EqualTo, InputRequired, Length, email_validator
from flask import request

class RegisterUserForm(FlaskForm):
    """
    注册表单
    validators: 验证器
    render_kw: 渲染属性
    """
    username = StringField(label="登录账号*", validators=[DataRequired('请输入登录账号'), Length(6, 64),
                                                      Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名只能使用字符串、数字和*%等特殊字符')],
                           render_kw={"class": 'form-control', "placeholder": "请输入登录账号", "required": 'required'})
    real_name = StringField(label="真实姓名*", validators=[DataRequired('请输入姓名')], render_kw={"class": 'form-control', "placeholder": "请输入姓名", })
    email = StringField(label="邮箱*", validators=[DataRequired('请输入邮箱'), Email('邮箱格式不正确')],
                        render_kw={"class": 'form-control', "placeholder": "请输入正确的邮箱地址以便接收信息", "required": 'required'})
    password = PasswordField(label="密码*", validators=[InputRequired(), EqualTo('password2', message='两次密码不一致')],
                             render_kw={"class": 'form-control', "placeholder": "请输入至少6位密码", "minlength": "6", "required": 'required'})
    password2 = PasswordField(label="确认密码*", validators=[InputRequired()], render_kw={"class": 'form-control', "placeholder": "确认密码", "required": 'required'})
    password_hint = StringField(label="密码提示", render_kw={"class": 'form-control'})
    submit = SubmitField(label="注册", render_kw={"class": "form-control btn btn-success"})

    @staticmethod
    def validate_account(calv):
        from ..model.auth_user import User
        check = User.query.filter_by(account=calv.data).first()
        if check:
            raise ValidationError("账号已经存在")

class BaseForm(Form):
    def __init__(self):
        data = request.get_json()
        args = request.args.to_dict()
        super(BaseForm, self).__init__(data=data, **args)
    
    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            raise ValidationError()
        return self

class UserForm(BaseForm):
    username = StringField('Username', validators=[Length(max=64)])
    password = PasswordField('Password', validators=[Length(8,16)])
        
    def get_user(self):
        from ..model.auth_user import User
        user = User.query.filter(User.name == self.username.data).first()
        return user
    
    def validate_username(self, field):
        if not self.get_user():
            raise ValidationError('Invalid username!')
    
    def validate_password(self, field):
        if not self.get_user():
            return 
        if not self.get_user().check_password(field.data):
            raise ValidationError('Incorrect password!')