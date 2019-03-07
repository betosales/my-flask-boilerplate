from project.server.api.auth.models import User
from .base import BaseTests


class TestUser(BaseTests):
    def test_check_password(self):
        user = User('test@test.com', 'correct')
        self.assertTrue(user.check_password('correct'))
        self.assertFalse(user.check_password('wrong password'))

    def test_email_and_password_required(self):
        self.assertRaises(TypeError, User)
        self.assertRaises(TypeError, User, email='test@test.com')
        self.assertRaises(TypeError, User, password='correct')

    def test_user_admin_none_raises(self):
        self.assertRaises(TypeError, User, email='test@test.com', password='correct', admin=None)

    def test_user_email_too_long(self):
        email = '{}@{}.com'.format('a' * 10, 'b'*255)
        self.assertRaises(AttributeError, User, email=email, password='correct')

    def test_user_password_too_long(self):
        password = 'c'*256
        self.assertRaises(AttributeError, User, email='test@test.com', password=password)
