import time

from project.server.api.auth.models import User, TokenBlacklist
from .base import BaseTests
import datetime
from project.server.api.auth.services.token_blacklist import (
    _epoch_utc_to_datetime, revoked_token, is_token_revoked, add_token_to_database, revoke_all_active_user_tokens,
    prune_all_expired_tokens, revoke_single_token)
from flask.wrappers import Response

from flask_jwt_extended import decode_token, create_access_token

from project.server import db


class TokenBlacklistTest(BaseTests):
    def test_epoch_utc_to_datetime(self):
        first_march_2019_epoch = 1551409200
        first_march_2019_date = datetime.datetime(2019, 3, 1)
        self.assertEqual(first_march_2019_date, _epoch_utc_to_datetime(first_march_2019_epoch))

    def test_revoked_token_status_code_401(self):
        rt = revoked_token()
        self.assertEqual(401, rt.status_code)

    def test_revoked_token_returns_valid_flask_response(self):
        rt = revoked_token()
        self.assertEqual(Response, type(rt))

    def test_revoked_token_returns_valid_response(self):
        rt = revoked_token()
        rt_json = rt.get_json()
        self.assertIn('status', rt_json)
        self.assertIn('msg', rt_json)
        self.assertEqual('fail', rt_json['status'])

    def test_is_token_revoked_no_result_found(self):
        token = create_access_token(
                identity=99999,
                fresh=True,
                expires_delta=datetime.timedelta(seconds=1))
        decoded_token = decode_token(token)
        self.assertTrue(is_token_revoked(decoded_token))

    def test_revoke_all_active_user_tokens(self):
        user = User('test@test.com', 'password')
        db.session.add(user)
        db.session.commit()
        token = create_access_token(
            identity=user.uuid,
            fresh=True,
            expires_delta=datetime.timedelta(seconds=60))
        add_token_to_database(token, user.id)
        active_tokens = TokenBlacklist.query.filter_by(user_id=user.id).filter_by(active=True)
        self.assertGreater(active_tokens.count(), 0)
        revoke_all_active_user_tokens(user.id)
        active_tokens = TokenBlacklist.query.filter_by(user_id=user.id).filter_by(active=True)
        self.assertEqual(active_tokens.count(), 0)

    def test_prune_all_expired_tokens(self):
        user = User('test_will_be@revoketed.com', 'password')
        db.session.add(user)
        db.session.commit()
        token = create_access_token(
            identity=user.uuid,
            fresh=True,
            expires_delta=datetime.timedelta(seconds=1))
        add_token_to_database(token, user.id)
        token = create_access_token(
            identity=user.uuid,
            fresh=True,
            expires_delta=datetime.timedelta(seconds=1))
        add_token_to_database(token, user.id)
        token = create_access_token(
            identity=user.uuid,
            fresh=True,
            expires_delta=datetime.timedelta(seconds=1))
        add_token_to_database(token, user.id)

        time.sleep(2)

        now = datetime.datetime.now()
        expired_tokens = TokenBlacklist.query.filter(TokenBlacklist.expires < now).all()
        self.assertGreater(len(expired_tokens), 0)
        prune_all_expired_tokens()
        expired_tokens = TokenBlacklist.query.filter(TokenBlacklist.expires < now).all()
        self.assertEqual(len(expired_tokens), 0)

    def test_revoke_single_token_with_valid_token(self):
        token = create_access_token(
            identity=999,
            fresh=True,
            expires_delta=datetime.timedelta(seconds=1))
        add_token_to_database(token, 999)
        decoded_token = decode_token(token)
        self.assertTrue(revoke_single_token(decoded_token['jti']))

    def test_revoke_single_token_with_invalid_token(self):
        self.assertFalse(revoke_single_token('invalid_token'))