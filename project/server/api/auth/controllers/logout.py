# -*- coding: utf-8 -*-
from flask import make_response, jsonify, request
from flask.views import MethodView

from flask_jwt_extended import jwt_required, get_raw_jwt

from project.server.api.auth.services.token_blacklist import revoke_single_token


class LogoutView(MethodView):
    """
    User Logout Resource
    """
    decorators = [jwt_required]

    def post(self):
        # import pdb; pdb.set_trace()
        decoded_token = get_raw_jwt()

        if 'jti' in decoded_token:
            revoke_single_token(decoded_token['jti'])

        response_object = {
            'status': 'success',
            'message': 'Logout successful'
        }
        return make_response(jsonify(response_object)), 200

