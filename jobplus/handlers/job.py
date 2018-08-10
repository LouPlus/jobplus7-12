# 职位路由
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from jobplus.models import Job, db

job = Blueprint('job', __name__, url_prefix= '/job')

@job.route('/')
def index():
	page = request.args.get('page', 1 , type=int)
	pagination = Job.query.filter(Job.is_disable.is_(False)).order_by(Job.created_at.desc()).paginate(
		page=page,
		per_page = 12,
		error_out=False,
	)
	return render_template('job/index.html', pagination=pagination, active='job')


@job.route('/<int:job_id>')
def detail(job_id):
	job = Job.query.get_or_404(job_id)
	return render_template('job/detail.html', job=job, active='')