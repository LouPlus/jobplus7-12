from flask_wtf import FlaskForm
from flask import url_for
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, ValidationError, SelectField
from wtforms.validators import Length, Email, EqualTo, Required, URL, NumberRange
from flask_uploads import UploadSet, DOCUMENTS
import os
from jobplus.models import db, User, Company, Job


set_resume = UploadSet('DOC', DOCUMENTS)


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(3, 24)])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
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
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱未注册')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')


class UserProfileForm(FlaskForm):
    real_name = StringField('姓名')
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    phone = StringField('手机号')
    work_years = IntegerField('工作年限')
    resume = FileField('简历上传', validators=[Required(), FileAllowed(set_resume, '只能上传文件！')])
    submit = SubmitField('提交')

    def validate_phone(self, field):
        phone = field.data
        if phone[:2] not in ('13', '15', '18') and len(phone) != 11:
            raise ValidationError('请输入有效的手机号')

    def name_resume(self):  # To avoid conflict with multiple resumes
        extension = os.path.splitext(self.resume.data.filename)[1]
        return self.real_name.data + self.phone.data + extension

    def updated_profile(self, user):
        user.real_name = self.real_name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data
        user.phone = self.phone.data
        user.work_years = self.work_years.data
        user.upload_resume_url = url_for('static', filename='resumes/' + self.name_resume(),
                                         _external=True)  # _external option depend absolute or relative link
        db.session.add(user)
        db.session.commit()


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
        if user.company_detail:
            company = user.company_detail
        else:
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

class UserEditForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码')
    real_name = StringField('姓名')
    phone = StringField('手机号')
    submit = SubmitField('提交')

    def update(self, user):
        self.populate_obj(user)
        if self.password.data:
            user.password = self.password.data
        db.session.add(user)
        db.session.commit()


class CompanyEditForm(FlaskForm):
    name = StringField('企业名称')
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码')
    phone = StringField('手机号')
    site = StringField('公司网站', validators=[Length(0, 64)])
    description = StringField('一句话简介', validators=[Length(0, 100)])
    submit = SubmitField('提交')

    def update(self, company):
        company.name = self.name.data
        company.email = self.email.data
        if self.password.data:
            company.password = self.password.data
        if company.detail:
            detail = company.detail
        else:
            detail = CompanyDetail()
            detail.user_id = company.id
        detail.site = self.site.data
        detail.description = self.description.data
        db.session.add(company)
        db.session.add(detail)
        db.session.commit()
class JobForm(FlaskForm):
    name = StringField('职位名称')
    salary_low = IntegerField('最低薪酬')
    salary_high = IntegerField('最高薪酬')
    location = StringField('工作地点')
    tags = StringField('职位标签(多个用，隔开)')
    experience_requirement = SelectField(
        '经验要求',
        choices=[
            ('不限', '不限'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('1-3', '1-3'),
            ('3-5', '3-5'),
            ('5+', '5+')
        ]
    )
    degree_requirement = SelectField(
        '学历要求',
        choices=[
            ('不限', '不限'),
            ('专科', '专科'),
            ('本科', '本科'),
            ('硕士', '硕士'),
            ('博士', '博士')
        ]
    )
    description = TextAreaField('职位描述', validators=[Length(0, 1500)])
    submit = SubmitField('发布')

    def create_job(self, company):
        job = Job()
        self.populate_obj(job)
        job.company_id = company.id
        db.session.add(job)
        db.session.commit()
        return job

    def update_job(self, job):
        self.populate_obj(job)
        db.session.add(job)
        db.session.commit()
        return job
