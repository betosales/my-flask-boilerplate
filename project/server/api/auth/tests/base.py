# -*- coding: utf-8 -*-
import unittest
from project.server import app, db
from project.server.api.auth.models import User


class BaseTests(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        # db.create_all()

    def tearDown(self):
        db.session.remove()
        # db.drop_all()
        self.app_context.pop()

    def createRoles(self):
        self.dropRoles()
        self.admin = User('admin@admin.com', 'admin', admin=True)
        db.session.add(self.admin)
        self.user = User('user@user.com', 'user')
        db.session.add(self.user)
        db.session.commit()

    def dropRoles(self):
        users = User.query.all()
        for user in users:
            db.session.delete(user)
        db.session.commit()

