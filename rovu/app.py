# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask

from rovu import public
from rovu.extensions import bcrypt, cache, db, debug_toolbar, login_manager, migrate
from rovu.settings import ProdConfig
from rovu.api.v1 import users
from rovu.api.v1 import events


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(users.views.blueprint)
    app.register_blueprint(events.views.blueprint)
    return None
