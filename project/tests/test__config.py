import unittest

from flask import current_app
from flask_testing import TestCase

from project.server import app


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.server.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertNotEqual(app.config['SECRET_KEY'], 'my_precious')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertEqual(
            app.config['SQLALCHEMY_DATABASE_URI'], 'postgresql:' +
            '//rsales:4br4c4d4br4@localhost/poc_login'
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.server.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertNotEqual(app.config['SECRET_KEY'], 'my_precious')
        self.assertTrue(app.config['DEBUG'])
        self.assertEqual(
            app.config['SQLALCHEMY_DATABASE_URI'], 'postgresql:' +
            '//rsales:4br4c4d4br4@localhost/poc_login_test'
        )


if __name__ == '__main__':
    unittest.main()
