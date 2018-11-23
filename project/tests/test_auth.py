import json
import unittest

import time

from project.server import db
from project.server.models import User, BlacklistToken
from project.tests.base import BaseTestCase


class TestAuthBlueprint(BaseTestCase):

    def register_user(self, email, password):
        return self.client.post(
            '/auth/register',
            data=json.dumps(dict(
                email=email,
                password=password
            )),
            content_type='application/json',
        )

    def login_user(self, email, password):
        return self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email=email,
                    password=password,
                    testing=True
                )),
                content_type="application/json"
            )

    def test_registration(self):
        """Test for user registration."""
        with self.client:
            response = self.register_user('joe@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['message'], 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_registered_with_already_registered_user(self):
        """Test registration with already registered email."""
        user = User(
            email='joe@gmail.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.register_user('joe@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(
                data['message'],
                'User already exists. Please Log in.'
            )
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.status_code, 202)

    def test_registered_user_login(self):
        """Test for login of registered-user login."""
        with self.client:
            # user registration
            resp_register = self.register_user('joe@gmail.com', '123456')
            data_register = json.loads(resp_register.data.decode())
            # registered user login
            response = self.login_user('joe@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['message'], 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_non_registered_user_login(self):
        """Test for login of non-registered user."""
        with self.client:
            response = self.login_user('joe@gmail.com', '123456')
            self.login_user('joe@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'User does not exist.')
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_registered_user_login_with_wrong_password(self):
        """Test for login of registered user with wrong password."""
        with self.client:
            # register user
            resp_register = self.register_user('joe@gmail.com', '123456')
            data_register = json.loads(resp_register.data.decode())
            # login
            resp_login = self.login_user('joe@gmail.com', 'wrong password')
            data = json.loads(resp_login.data.decode())
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(
                data['message'],
                'User does not exist.'
            )
            self.assertEqual(resp_login.content_type, 'application/json')
            self.assertEqual(resp_login.status_code, 404)

    def test_user_status(self):
        """Test for user status."""
        with self.client:
            resp_register = self.register_user('joe@gmail.com', '123456')
            response = self.client.get(
                '/auth/status',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'success')
            self.assertIsNotNone(data['data'])
            self.assertEqual(data['data']['email'], 'joe@gmail.com')
            self.assertIn(data['data']['admin'], [True, False])
            self.assertEqual(response.status_code, 200)

    def test_valid_logout(self):
        """Test for logout before token expires."""
        with self.client:
            # user registration
            resp_register = self.register_user('joe@gmail.com', '123456')
            data_register = json.loads(resp_register.data.decode())
            # user login
            # registered user login
            resp_login = self.login_user('joe@gmail.com', '123456')
            data = json.loads(resp_login.data.decode())
            # valid token logout
            resp_logout = self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(resp_logout.data.decode())
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['message'], 'Successfully logged out.')
            self.assertEqual(resp_logout.status_code, 200)

    def test_invalid_logout(self):
        """ Testing logout after the token expires """
        with self.client:
            # user registration
            resp_register = self.register_user('joe@gmail.com', '123456')
            data_register = json.loads(resp_register.data.decode())
            # user login
            resp_login = self.login_user('joe@gmail.com', '123456')
            data_login = json.loads(resp_login.data.decode())
            # invalid token logout
            time.sleep(6)
            response = self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Signature expired. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_valid_blacklisted_token_logout(self):
        """ Test for logout after a valid token gets blacklisted """
        with self.client:
            # user registration
            resp_register = self.register_user('joe@gmail.com', '123456')
            data_register = json.loads(resp_register.data.decode())
            # user login
            resp_login = self.login_user('joe@gmail.com', '123456')
            data_login = json.loads(resp_login.data.decode())
            # blacklist a valid token
            blacklist_token = BlacklistToken(
                token=json.loads(resp_login.data.decode())['auth_token'])
            db.session.add(blacklist_token)
            db.session.commit()
            # blacklisted valid token logout
            response = self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(
                data['status'],
                'fail'
            )
            self.assertEqual(
                data['message'],
                'Token blacklisted. Please log in again.'
            )
            self.assertEqual(response.status_code, 401)

    def test_valid_blacklisted_token_user(self):
        """Test for user status with a blacklisted valid token."""
        with self.client:
            # user registration
            resp_register = self.register_user('joe@gmail.com', '123456')
            # blacklist a valid token
            blacklist_token = BlacklistToken(
                token=json.loads(resp_register.data.decode())['auth_token'])
            db.session.add(blacklist_token)
            db.session.commit()
            response = self.client.get(
                '/auth/status',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(
                data['message'],
                'Token blacklisted. Please log in again.'
            )
            self.assertEqual(response.status_code, 401)

    def test_user_status_malformed_bearer_token(self):
        """ Test for user status with malformed bearer token"""
        with self.client:
            resp_register = self.register_user('joe@gmail.com', '123456')
            response = self.client.get(
                '/auth/status',
                headers=dict(
                    Authorization='Bearer' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Bearer token malformed.')
            self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
