# -*- coding: utf-8 -*
# 主页的路由
from flask import Blueprint, render_template, current_app, flash, redirect, url_for

from flask_login import login_required, login_user, logout_user
from jobplus.models import db, User, Company, Job
from jobplus.forms import RegisterForm, LoginForm

front = Blueprint('front', __name__)


@front.route('/')
def index():
    newest_jobs = Job.query.filter(Job.is_disable.is_(False)).order_by(Job.created_at.desc()).limit(9)
    newest_companies = User.query.filter(
        User.role == User.ROLE_COMPANY
    ).order_by(User.created_at.desc()).limit(8)
    return render_template(
        'index.html',
        active='index',
        newest_jobs = newest_jobs,
        newest_companies = newest_companies,
    )


@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)

        company = Company.query.filter_by(user_id=user.id).first()
        if user.is_company and company is None:
            #企业用户第一次登录跳转企业信息页面
            return redirect(url_for('company.profile'))        
        
        elif user.is_company and company is not None:
            #企业用户非首次登录跳转主页面
            return redirect(url_for('.index'))
        
        else:
        
            next = 'user.profile'
            if user.is_admin:
                next = 'admin.index'
            return redirect(url_for(next))    

    return render_template('login.html', form=form)



        

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登录', 'success')
    return redirect(url_for('.index'))


@front.route('/register_user', methods=['GET','POST'])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user(10)
        flash('注册成功', 'success')
        return redirect(url_for('front.login'))
    return render_template('register_user.html', form=form)


@front.route('/register_company', methods=['GET', 'POST'])
def register_company():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user(20)
        flash('注册成功', 'success')
        return redirect(url_for('front.login'))
    return render_template('register_company.html', form=form)
