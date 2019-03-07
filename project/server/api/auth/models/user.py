# -*- coding: utf-8 -*-
from project.server import db, bcrypt
from project.server.api.auth.services.uuid import generate_uuid

from .base import Base


class User(Base):
    """User Model for storing user related details."""

    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    uuid = db.Column(db.String, name="uuid", primary_key=True,
                     default=generate_uuid)

    def __init__(self, email, password, admin=False):
        """
        Initialize an user.

        :param email:
        :param password:
        :param admin:
        """
        if type(admin) is not bool:
            raise TypeError
        if len(email) > 255:
            raise AttributeError('email too long')
        if len(password) > 255:
            raise AttributeError('password too long')
        # TODO check if email format is valid
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode()
        self.admin = admin

    def check_password(self, password):
        """
        Check if password is correct, returns boolean.

        :param password:
        """
        return bcrypt.check_password_hash(self.password, password)
