# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user

from rovu.extensions import login_manager
from rovu.api.v1.users.models import User
from rovu.utils import flash_errors

from .forms import LoginForm

blueprint = Blueprint('public', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/', methods=['GET'])
def index():
    """landing page."""
    return render_template('index.html')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """login page."""
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            redirect_url = request.args.get('next') or url_for('admin.index')
            print(redirect_url)
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template('login.html', form=form)
