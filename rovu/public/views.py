# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, render_template
from flask_login import login_required, login_user, logout_user

from rovu.extensions import login_manager
from rovu.api.v1.users.models import User

blueprint = Blueprint('public', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/', methods=['GET'])
def index():
    """landing page."""
    return render_template('index.html')
