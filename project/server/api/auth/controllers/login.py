# -*- coding: utf-8 -*-
from flask import make_response, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta

from project.server.api.auth.models import User
from project.server.api.auth.services.token_blacklist import add_token_to_database, revoke_all_active_user_tokens


class LoginView(MethodView):
    """
    User Login Resource
    """
    def post(self):
        # get the post data
        post_data = request.get_json()
        if not post_data:
            response_object = {
                'status': 'fail',
                'message': 'Empty payload is not allowed.'
            }
            return make_response(jsonify(response_object)), 500

        if 'email' not in post_data or 'password' not in post_data:
            response_object = {
                'status': 'fail',
                'message': 'email or password not found.'
            }
            return make_response(jsonify(response_object)), 500

        # fetch the user data
        user = User.query.filter_by(
            email=post_data.get('email')
        ).first()
        if user and user.check_password(post_data.get('password')):
            auth_token = create_access_token(
                identity=user.uuid,
                fresh=True,
                expires_delta=timedelta(days=1))
            refresh_token = create_refresh_token(
                identity=user.uuid,
                expires_delta=timedelta(days=30))
            if auth_token:
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token,
                    'refresh_token': refresh_token
                }
                revoke_all_active_user_tokens(user.id)
                add_token_to_database(auth_token, user.id)
                add_token_to_database(refresh_token, user.id)
                return make_response(jsonify(response_object)), 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'User and Password does not exist.'
            }
            return make_response(jsonify(response_object)), 404
