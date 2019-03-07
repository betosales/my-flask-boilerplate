# -*- coding: utf-8 -*-
import unittest
from os import environ


class TestEnvironmentVariables(unittest.TestCase):

    def test_secret_key_exists(self):
        self.assertIsNotNone(environ.get('SECRET_KEY'))

    def test_connection_url_exists(self):
        self.assertIsNotNone(environ.get('CONNECTION_URL'))

    def test_flask_env_exists(self):
        self.assertIsNotNone(environ.get('FLASK_ENV'))

    def test_database_name_exists(self):
        self.assertIsNotNone(environ.get('DATABASE_NAME'))

    def test_app_settings_exists(self):
        self.assertIsNotNone(environ.get('APP_SETTINGS'))
