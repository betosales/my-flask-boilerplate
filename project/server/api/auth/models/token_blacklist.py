# -*- coding: utf-8 -*-
from project.server import db
from .base import Base


class TokenBlacklist(Base):
    __tablename__ = "tokens_blacklist"
    __table_args__ = {'extend_existing': True}

    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    expires = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
