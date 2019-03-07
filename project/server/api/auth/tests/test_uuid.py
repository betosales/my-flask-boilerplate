# -*- coding: utf-8 -*-
import unittest
from project.server.api.auth.services.uuid import generate_uuid
import uuid


class UUIDTest(unittest.TestCase):
    def test_generate_uuid_returns_UUID4(self):
        my_uuid = generate_uuid()
        my_wrong_uuid = my_uuid[:-1]
        self.assertRaises(ValueError, uuid.UUID, my_wrong_uuid, version=4)
        val = uuid.UUID(my_uuid, version=4)
        self.assertEqual(my_uuid, str(val))
