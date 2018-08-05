from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, ValidationError
from wtforms.validators import Length, Email, EqualTo, Required, URL, NumberRange
from jobplus.models import db, User, Company

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(3, 24)])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6,24)])
    repeat_password = PasswordField('重复密码', validators=[Required(), EqualTo('password')])
    submit = SubmitField('提交')

    def create_user(self, role):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        user.role = role
        db.session.add(user)
        db.session.commit()
        return user
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户存在')
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱存在')
    

class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6,24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')
    def validate_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱未注册')
    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')


class CompanyProfileForm(FlaskForm):
    username = StringField('企业名称')
    email = StringField('邮箱', validators=[Required(),Email()])
    password = PasswordField('密码（不填保持不变）')
    slug = StringField('Slug', validators=[Required(),Length(3,24)])
    location = StringField('地址', validators=[Required(),Length(0,64)])
    site = StringField('公司网站', validators=[Length(0,64)])
    logo = StringField('Logo')
    description = StringField('一句话描述', validators=[Length(0,100)])
    about = TextAreaField('公司详情', validators=[Length(0,1024)])
    submit = SubmitField('提交')

    def updated_profile(self, user):
        user.username = self.username.data
        user.email = self.email.data

        if self.password.data:
            user.password = self.password.data
        
        company = Company()
        company.user_id = user.id
        
        if self.slug.data:
            company.slug = self.slug.data
        if self.location.data:
            company.location = self.location.data
        if self.site.data:
            company.site = self.site.data
        if self.logo.data:
            company.logo = self.logo.data
        if self.description.data:
            company.description = self.description.data
        if self.about.data:
            company.about = self.about.data
        

        db.session.add(user)
        db.session.add(company)
        db.session.commit()
