# Copyright (C) 2017 O.S. Systems Software LTDA.
# This software is released under the MIT License

import base64
import json
import unittest
from datetime import datetime, timedelta

from jose import jwt

from hydra import Hydra, JWK


class ChallengeTestCase(unittest.TestCase):

    def setUp(self):
        self.hydra = Hydra('http://localhost:4444', 'client', 'secret')
        self.jti = '64c4f79e-e016-45b8-8c0e-d96c671c1e8a'
        self.exp = datetime.utcnow() + timedelta(minutes=10)
        self.ext = {'foo': 'bar'}
        self.aud = 'client'
        self.scp = ['core', 'hydra']
        self.challenge_data = {
            'aud': self.aud,
            'exp': self.exp,
            'jti': self.jti,
            'redir': 'https://192.168.99.100:4444/',
            'scp': self.scp,
        }
        jwk = self.hydra.jwk.get('hydra.consent.challenge', JWK.PRIVATE)
        self.challenge = jwt.encode(
            self.challenge_data, jwk.to_rsa(), algorithm='RS256')

    def test_can_decode_challenge(self):
        challenge = self.hydra.challenge_decode(self.challenge)
        self.assertEqual(challenge, self.challenge_data)

    def test_can_encode_challenge(self):
        response = self.hydra.challenge_encode(
            self.challenge_data, sub='foo', uname='bar', at_ext=self.ext)
        challenge = json.loads(
            base64.urlsafe_b64decode(response.split('.')[1] + '==').decode())
        self.assertEqual(challenge['sub'], 'foo')
        self.assertEqual(challenge['uname'], 'bar')
        self.assertIsNotNone(challenge['iat'])
        self.assertEqual(challenge['aud'], self.aud)
        self.assertEqual(challenge['at_ext'], self.ext)
        self.assertEqual(challenge['scp'], self.scp)
