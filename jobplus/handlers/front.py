# -*- coding: utf-8 -*
# 主页的路由
from flask import Blueprint, render_template

front = Blueprint('front', __name__)
@front.route('/')
def index():
	return render_template('index.html')