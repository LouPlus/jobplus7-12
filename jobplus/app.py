# -*- coding: utf-8 -*
from flask import Flask, render_template
from jobplus.config import configs
from flask_migrate import Migrate
from jobplus.models import db, User
from flask_login import LoginManager
from flask_uploads import configure_uploads, patch_request_class
from jobplus.forms import set_resume


def register_blueprints(app):
    from .handlers import front, admin, user, company, job
    app.register_blueprint(front)
    #app.register_blueprint(admin)
    app.register_blueprint(user)
    app.register_blueprint(company)
    #app.register_blueprint(job)


def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    login_manager.login_view = 'front.login'


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    register_blueprints(app)
    register_extensions(app)
    app.config['UPLOADED_DOC_DEST'] = './jobplus/static/resumes'  # upload DOC directory
    configure_uploads(app, set_resume)
    patch_request_class(app)  # set maximum file size, default 16MB
    return app
