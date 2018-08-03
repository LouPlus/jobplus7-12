from flask import Blueprint, render_template, current_app, flash, redirect, url_for
from jobplus.decorators import company_required

company = Blueprint('company', __name__, url_prefix='/company')

@company.route('/profile')
@company_required
def profile():
	return render_template('company/profile.html')
