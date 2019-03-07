# -*- coding: utf-8 -*-
import unittest
import datetime

from flask_jwt_extended import create_access_token

from project.server.api.auth.services.token_blacklist import add_token_to_database
from .base import BaseTests


class LogoutTests(BaseTests):
    def setUp(self):
        super().setUp()
        self.createRoles()

    def test_logout(self):
        payload = {
            'email': 'user@user.com',
            'password': 'user'
        }
        response_login = self.client.post('/auth/login', json=payload)
        self.assertEqual(response_login.status_code, 200)
        response_login_json = response_login.get_json()
        auth_token = response_login_json['auth_token']

        response_index = self.client.get('/',
                                         headers={"Authorization": f"Bearer {auth_token}"})
        self.assertEqual(response_index.status_code, 200)
        self.assertEqual(response_index.get_json()['status'], 'success')

        response = self.client.post('/auth/logout',
                                    headers={"Authorization": f"Bearer {auth_token}"})
        self.assertEqual(response.status_code, 200)
        response_json = response.get_json()
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['message'], 'Logout successful')

