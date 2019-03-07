# -*- coding: utf-8 -*-
from .base import BaseTests


class IndexTests(BaseTests):
    def setUp(self):
        super().setUp()
        self.createRoles()

    def test_index_status_code_200(self):
        payload = {
            'email': 'user@user.com',
            'password': 'user'
        }
        response_login = self.client.post('/auth/login', json=payload)
        response_login_json = response_login.get_json()
        auth_token = response_login_json['auth_token']
        response = self.client.get('/',
                                   headers={"Authorization": f"Bearer {auth_token}"})
        self.assertEqual(response.status_code, 200)
        response_json = response.get_json()
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['message'], 'Deu certo, você conseguiu entrar')
