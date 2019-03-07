# -*- coding: utf-8 -*-
from flask import Blueprint

from .controllers.login import LoginView
from .controllers.logout import LogoutView

bp_auth = Blueprint('auth', __name__, url_prefix='/auth')

# endpoints
login_view = LoginView.as_view('login_api')
logout_view = LogoutView.as_view('logout_api')

# rules for endpoints
bp_auth.add_url_rule(
    '/login',
    view_func=login_view,
    endpoint='login'
)
bp_auth.add_url_rule(
    '/logout',
    view_func=logout_view,
    endpoint='logout'
)

