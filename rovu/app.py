# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_graphql import GraphQLView
from flask_login import current_user

from rovu import public, models
from rovu.extensions import (bcrypt, cache, db, debug_toolbar, login_manager,
                             migrate)
from rovu.settings import ProdConfig
from rovu.api.v1 import events
from rovu.api.v2.events.schema import schema


def create_app(config_object=ProdConfig):
    """An application factory,
    as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_admin(app)
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
    app.register_blueprint(events.views.blueprint)
    app.add_url_rule('/api/v2/graphql',
                     view_func=GraphQLView.as_view('graphql',
                                                   schema=schema,
                                                   graphiql=True))
    return None


def register_admin(app):
    """Register the admin routes."""
    class AdminView(ModelView):
        def is_accessible(self):
            return current_user.is_authenticated

        def inaccessible_callback(self, name, **kwargs):
            return redirect(url_for('public.index'))

    admin = Admin(app, name='JoynUp', template_mode='bootstrap3')
    admin.add_view(AdminView(models.User, db.session))
    admin.add_view(AdminView(models.Event, db.session))
    admin.add_view(AdminView(models.Role, db.session))
    return None
