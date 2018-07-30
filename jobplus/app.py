# -*- coding: utf-8 -*
from flask import Flask, render_template
from jobplus.config import configs

def register_blueprints(app):
    from .handlers import front
    app.register_blueprint(front)

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    register_blueprints(app)
    return app

