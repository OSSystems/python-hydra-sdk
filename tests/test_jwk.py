# Copyright (C) 2017 O.S. Systems Software LTDA.
# This software is released under the MIT License

import json
import unittest
from unittest.mock import patch

from Crypto.PublicKey.RSA import RsaKey

from hydra import Hydra, JWK
from hydra.exceptions import HydraResponseError, HydraRequestError


class JWKTestCase(unittest.TestCase):

    def setUp(self):
        self.private_key = {
            'kty': 'RSA',
            'n': '0vx7agoebGcQSuuPiLJXZptN9nndrQmbXEps2aiAFbWhM78LhWx4cbbfAAtVT86zwu1RK7aPFFxuhDR1L6tSoc_BJECPebWKRXjBZCiFV4n3oknjhMstn64tZ_2W-5JsGY4Hc5n9yBXArwl93lqt7_RN5w6Cf0h4QyQ5v-65YGjQR0_FDW2QvzqY368QQMicAtaSqzs8KJZgnYb9c7d0zgdAZHzu6qMQvRL5hajrn1n91CbOpbISD08qNLyrdkt-bFTWhAI4vMQFh6WeZu0fM4lFd2NcRwr3XPksINHaQ-G_xBniIqbw0Ls1jF44-csFCur-kEgU8awapJzKnqDKgw',  # nopep8
            'e': 'AQAB',
            'd': 'X4cTteJY_gn4FYPsXB8rdXix5vwsg1FLN5E3EaG6RJoVH-HLLKD9M7dx5oo7GURknchnrRweUkC7hT5fJLM0WbFAKNLWY2vv7B6NqXSzUvxT0_YSfqijwp3RTzlBaCxWp4doFk5N2o8Gy_nHNKroADIkJ46pRUohsXywbReAdYaMwFs9tv8d_cPVY3i07a3t8MN6TNwm0dSawm9v47UiCl3Sk5ZiG7xojPLu4sbg1U2jx4IBTNBznbJSzFHK66jT8bgkuqsk0GjskDJk19Z4qwjwbsnn4j2WBii3RL-Us2lGVkY8fkFzme1z0HbIkfz0Y6mqnOYtqc0X4jfcKoAC8Q',  # nopep8
            'alg': 'RS256',
            'kid': '2011-04-29',
        }
        self.public_key = {
            'kty': 'RSA',
            'alg': 'RS256',
            'kid': '2011-04-29',
            'n': '0vx7agoebGcQSuuPiLJXZptN9nndrQmbXEps2aiAFbWhM78LhWx4cbbfAAtVT86zwu1RK7aPFFxuhDR1L6tSoc_BJECPebWKRXjBZCiFV4n3oknjhMstn64tZ_2W-5JsGY4Hc5n9yBXArwl93lqt7_RN5w6Cf0h4QyQ5v-65YGjQR0_FDW2QvzqY368QQMicAtaSqzs8KJZgnYb9c7d0zgdAZHzu6qMQvRL5hajrn1n91CbOpbISD08qNLyrdkt-bFTWhAI4vMQFh6WeZu0fM4lFd2NcRwr3XPksINHaQ-G_xBniIqbw0Ls1jF44-csFCur-kEgU8awapJzKnqDKgw',  # nopep8
            'e': 'AQAB',
        }

    def test_can_create_private_JWK(self):
        jwk = JWK(**self.private_key)
        self.assertEqual(jwk.type, JWK.PRIVATE)
        self.assertEqual(jwk.kty, self.private_key['kty'])
        self.assertEqual(jwk.alg, self.private_key['alg'])
        self.assertEqual(jwk.n, self.private_key['n'])
        self.assertEqual(jwk.e, self.private_key['e'])
        self.assertEqual(jwk.d, self.private_key['d'])

    def test_can_create_public_JWK(self):
        jwk = JWK(**self.public_key)
        self.assertEqual(jwk.type, JWK.PUBLIC)
        self.assertEqual(jwk.kty, self.public_key['kty'])
        self.assertEqual(jwk.alg, self.public_key['alg'])
        self.assertEqual(jwk.n, self.public_key['n'])
        self.assertEqual(jwk.e, self.public_key['e'])

    def test_can_convert_base64_to_int(self):
        expected = 65537
        observed = JWK.b64_to_int('AQAB')
        self.assertEqual(observed, expected)

    def test_can_convert_to_RSA(self):
        jwk_public = JWK(**self.public_key)
        jwk_private = JWK(**self.private_key)
        self.assertIsInstance(jwk_public.to_rsa(), RsaKey)
        self.assertIsInstance(jwk_private.to_rsa(), RsaKey)


class JWKManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.hydra = Hydra('http://localhost:4444', 'client', 'secret')

    def test_can_get_private_key(self):
        key = self.hydra.jwk.get('hydra.consent.response', 'private')
        self.assertEqual(key.type, JWK.PRIVATE)
        self.assertIsNotNone(key.n)
        self.assertIsNotNone(key.e)
        self.assertIsNotNone(key.d)

    def test_can_get_public_key(self):
        key = self.hydra.jwk.get('hydra.consent.challenge', 'public')
        self.assertEqual(key.type, JWK.PUBLIC)
        self.assertIsNotNone(key.n)
        self.assertIsNotNone(key.e)

    @patch('requests.request')
    def test_raises_error_with_bad_request(self, request):
        request.return_value.ok = False
        with self.assertRaises(HydraRequestError):
            self.hydra.jwk.get('hydra.consent.challenge', 'public')

    @patch('requests.request')
    def test_raises_error_when_bad_response_content_type(self, request):
        effects = [{}, json.JSONDecodeError('', '', 0)]
        request.return_value.json.side_effect = effects
        with self.assertRaises(HydraResponseError):
            self.hydra.jwk.get('hydra.consent.challenge', 'public')

    @patch('requests.request')
    def test_raises_error_when_bad_response_content(self, request):
        request.return_value.json.return_value = {}
        with self.assertRaises(HydraResponseError):
            self.hydra.jwk.get('hydra.consent.challenge', 'public')

    @patch('requests.request')
    def test_raises_error_when_no_keys_are_provided(self, request):
        request.return_value.json.return_value = {'keys': []}
        with self.assertRaises(HydraResponseError):
            self.hydra.jwk.get('hydra.consent.challenge', 'public')
