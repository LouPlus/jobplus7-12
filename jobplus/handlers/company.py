# 企业路由

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from jobplus.forms import CompanyProfileForm
from jobplus.decorators import company_required

company = Blueprint('company', __name__, url_prefix='/company')

@company.route('/profile', methods=['GET','POST'])
@login_required
@company_required
def profile():

    form = CompanyProfileForm(obj=current_user.company_detail)
    form.username.data = current_user.username
    form.email.data = current_user.email

    if current_user.company_detail is not None:
        form.slug.data = current_user.company_detail.slug
        form.site.data = current_user.company_detail.site
        form.logo.data = current_user.company_detail.logo
        form.description.data = current_user.company_detail.description
        form.about.data = current_user.company_detail.about
    if form.validate_on_submit():
        form.updated_profile(current_user)
        flash('企业信息更新成功','success')
        return redirect(url_for('company.profile'))
    return render_template('/company/profile.html',form=form)



