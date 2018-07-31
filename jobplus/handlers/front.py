# -*- coding: utf-8 -*
# 主页的路由
from flask import Blueprint, render_template
from jobplus.forms import RegisterForm, LoginForm
front = Blueprint('front', __name__)
@front.route('/')
def index():
	return render_template('index.html')
@front.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	return render_template('login.html',form=form)
@front.route('/<reg>', methods=['GET','POST'])
def register(reg):
	form = RegisterForm()
	if reg == "register_user":
		return render_template('register.html',form=form)
	elif reg == "register_company":
		return render_template('register.html',form=form)
	else:
		return render_template('index.html')
