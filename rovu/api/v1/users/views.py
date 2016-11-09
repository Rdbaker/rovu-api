# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from rovu.api.v1.users.models import User
from rovu.api.v1.users.schema import UserSchema

blueprint = Blueprint('users', __name__, url_prefix='/api/v1/users')
USER_SCHEMA = UserSchema()


@blueprint.route('/', strict_slashes=False)
@login_required
def users():
    """List members."""
    return USER_SCHEMA.dumps(User.query.all(), many=True).data


@blueprint.route('/me', strict_slashes=False)
@login_required
def me():
    """List members."""
    return USER_SCHEMA.dumps(current_user).data
    return render_template('users/members.html')
