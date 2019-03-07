# -*- coding: utf-8 -*-
from datetime import datetime

from flask import make_response, jsonify
from sqlalchemy.orm.exc import NoResultFound

from project.server.api.auth.models import TokenBlacklist
from project.server import db
from flask_jwt_extended import decode_token


def _epoch_utc_to_datetime(epoch_utc):
    """
    Helper function for converting epoch timestamps (as stored in JWTs) into
    python datetime objects (which are easier to use with sqlalchemy).
    """
    return datetime.fromtimestamp(epoch_utc)


def is_token_revoked(decoded_token):
    """
    Checks if the given token is revoked or not. If the token is present
    in the database we are going to consider it revoked.
    """
    jti = decoded_token['jti']
    try:
        token = TokenBlacklist.query.filter_by(jti=jti).one()
        return not token.active
    except NoResultFound:
        return True


def revoked_token():
    """Return a message when a revoked token was provided."""
    response_object = {
        "status": "fail",
        "msg": "Token revoked, you must login again."}
    return make_response(jsonify(response_object), 401)


def register_headers(jwt):
    """Register all headers."""
    jwt.token_in_blacklist_loader(is_token_revoked)
    jwt.revoked_token_loader(revoked_token)


def add_token_to_database(encoded_token, user_id):
    """
    Adds a new token to the database. It is not revoked when it is added.
    :param encoded_token: token provided by jwt
    :param user_id: id of user
    """
    decoded_token = decode_token(encoded_token)
    jti = decoded_token['jti']
    token_type = decoded_token['type']
    expires = _epoch_utc_to_datetime(decoded_token['exp'])

    db_token = TokenBlacklist(
        jti=jti,
        user_id=user_id,
        token_type=token_type,
        expires=expires,
    )
    db.session.add(db_token)
    db.session.commit()


def revoke_all_active_user_tokens(user_id):
    """
    Revoke all active user tokens.
    :param user_id:
    """
    tokens = TokenBlacklist.query.filter_by(user_id=user_id).filter_by(active=True)
    for token in tokens:
        token.active = False
        db.session.add(token)
    db.session.commit()

    return True


def revoke_single_token(jti):
    """
    Revoke a single token.
    :param jti:
    :return bool:
    """
    tokens = TokenBlacklist.query.filter_by(jti=jti).filter_by(active=True)
    if tokens.count():
        for token in tokens:
            token.active = False
            db.session.add(token)
        db.session.commit()
        return True
    return False


def prune_all_expired_tokens():
    """Delete all expired tokens."""
    now = datetime.now()
    expired = TokenBlacklist.query.filter(TokenBlacklist.expires < now).all()
    for token in expired:
        db.session.delete(token)
    db.session.commit()
