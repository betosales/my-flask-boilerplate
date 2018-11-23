from flask import Blueprint

from .login import LoginView
from .logout import LogoutView
from .register import RegisterView
from .user_details import UserDetailsView

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

# define the endpoints
login_view = LoginView.as_view('login_api')
user_detail_view = UserDetailsView.as_view('user_api')
logout_view = LogoutView.as_view('logout_api')
register_view = RegisterView.as_view('register_api')

# add Rules for Endpoints
auth_blueprint.add_url_rule(
    '/register',
    view_func=register_view
)
auth_blueprint.add_url_rule(
    '/login',
    view_func=login_view
)
auth_blueprint.add_url_rule(
    '/status',
    view_func=user_detail_view
)
auth_blueprint.add_url_rule(
    '/logout',
    view_func=logout_view
)
