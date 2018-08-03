from flask import Blueprint, render_template, current_app, flash, redirect, url_for
from jobplus.decorators import user_required

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/profile')
@user_required
def profile():
	return render_template('user/profile.html')