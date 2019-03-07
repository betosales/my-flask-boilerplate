# -*- coding: utf-8 -*-
from .base import BaseTests


class LoginTests(BaseTests):
    def setUp(self):
        super().setUp()
        self.createRoles()

    def test_login_without_payload(self):
        response = self.client.post('/auth/login')
        self.assertEqual(response.status_code, 500)
        response_json = response.get_json()
        self.assertEqual(response_json['status'], 'fail')
        self.assertEqual(response_json['message'], 'Empty payload is not allowed.')

    def test_login_with_only_email(self):
        payload = {
            'email': 'user@user.com'
        }
        response = self.client.post('/auth/login', json=payload)
        self.assertEqual(response.status_code, 500)
        response_json = response.get_json()
        self.assertEqual(response_json['status'], 'fail')
        self.assertEqual(response_json['message'], 'email or password not found.')

    def test_login_with_only_password(self):
        payload = {
            'password': 'user'
        }
        response = self.client.post('/auth/login', json=payload)
        self.assertEqual(response.status_code, 500)
        response_json = response.get_json()
        self.assertEqual(response_json['status'], 'fail')
        self.assertEqual(response_json['message'], 'email or password not found.')

    def test_login_status_code_is_200(self):
        payload = {
            'email': 'user@user.com',
            'password': 'user'
        }
        response = self.client.post('/auth/login', json=payload)
        self.assertEqual(response.status_code, 200)
        response_json = response.get_json()
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['message'], 'Successfully logged in.')
        self.assertIn('auth_token', response_json)
        self.assertIn('refresh_token', response_json)

    def test_login_correct_email_wrong_password(self):
        payload = {
            'email': 'user@user.com',
            'password': 'wrong'
        }
        response = self.client.post('/auth/login', json=payload)
        self.assertEqual(response.status_code, 404)
        response_json = response.get_json()
        self.assertEqual(response_json['status'], 'fail')
        self.assertEqual(response_json['message'], 'User and Password does not exist.')

