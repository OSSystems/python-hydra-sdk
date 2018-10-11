# Copyright (C) 2017 O.S. Systems Software LTDA.
# This software is released under the MIT License

import unittest
from unittest.mock import patch

from hydra import Hydra


class HydraTestCase(unittest.TestCase):

    def setUp(self):
        self.hydra = Hydra('http://localhost:9000', 'http://localhost:9001',
                           'client', 'secret')

    def test_can_retrieve_access_token(self):
        token = self.hydra.get_access_token()
        self.assertIsNotNone(token)

    def test_can_instropect_token(self):
        token = self.hydra.get_access_token()
        result = self.hydra.instrospect_token(token)
        self.assertIsNotNone(result)
        self.assertTrue(result['active'])

    def test_can_revoke_token(self):
        token = self.hydra.get_access_token()
        instrospection = self.hydra.instrospect_token(token)
        self.assertTrue(instrospection['active'])

        response = self.hydra.revoke_token(token)

        self.assertTrue(response)
        instrospection = self.hydra.instrospect_token(token)
        self.assertFalse(instrospection['active'])
