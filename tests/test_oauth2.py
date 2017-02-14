# Copyright (C) 2017 O.S. Systems Software LTDA.
# This software is released under the MIT License

import unittest
from unittest.mock import Mock, patch

from hydra.oauth2 import Client, Token


class TokenTestCase(unittest.TestCase):

    def setUp(self):
        self.data = {
            'scope': 'hydra',
            'expires_in': 10,
            'access_token': 'super-token',
            'token_type': 'bearer'
        }

    def test_can_create_token(self):
        token = Token(**self.data)
        self.assertEqual(token.scope, 'hydra')
        self.assertEqual(token.expires_in, 10)
        self.assertEqual(token.token, 'super-token')
        self.assertEqual(token.type, 'bearer')

    def test_string_representation(self):
        token = Token(**self.data)
        expected = 'bearer super-token'
        self.assertEqual(str(token), expected)

    def test_token_is_expired(self):
        token = Token(**self.data)
        self.assertFalse(token.is_expired())

        self.data['expires_in'] = 0
        token = Token(**self.data)
        self.assertTrue(token.is_expired())


class ClientTestCase(unittest.TestCase):

    def setUp(self):
        self.data = {
            'host': 'http://localhost',
            'client': 'client',
            'secret': 'secret',
        }
        self.token_response = {
            'scope': 'devices',
            'expires_in': 10,
            'access_token': 'super-token',
            'token_type': 'bearer'
        }
        self.token = Token(**self.token_response)

    def test_can_create_client(self):
        c = Client(**self.data)
        self.assertEqual(c.host, 'http://localhost')
        self.assertEqual(c.client, 'client')
        self.assertEqual(c.secret, 'secret')

    @patch('requests.request')
    def test_request_with_basic_authentication(self, request):
        c = Client(**self.data)
        c.request(
            'POST', '/oauth2/token', token=False, json={'token': 'foobar'})
        request.assert_called_with(
            'POST', 'http://localhost/oauth2/token',
            auth=('client', 'secret'), json={'token': 'foobar'})

    @patch('requests.request')
    def test_request_with_token_authentication(self, request):
        request.return_value.json.return_value = self.token_response
        c = Client(**self.data)
        c.request('GET', '/clients', token=True)
        headers = {'Authorization': 'bearer super-token'}
        request.assert_called_with(
            'GET', 'http://localhost/clients', headers=headers)

    @patch('requests.request')
    def test_can_get_access_token(self, request):
        request.return_value.json.return_value = self.token_response
        c = Client(**self.data)
        token = c.get_access_token('devices')
        self.assertEqual(token.scope, 'devices')
        self.assertEqual(token.expires_in, 10)
        self.assertEqual(token.token, 'super-token')
        self.assertEqual(token.type, 'bearer')

    @patch('requests.request')
    def test_get_access_token_request_is_made_correctly(self, request):
        c = Client(**self.data)
        c.get_access_token()
        request.assert_called_with(
            'POST', 'http://localhost/oauth2/token',
            auth=(c.client, c.secret),
            data={'grant_type': 'client_credentials'})

        c.get_access_token('devices')
        request.assert_called_with(
            'POST', 'http://localhost/oauth2/token',
            auth=(c.client, c.secret),
            data={'grant_type': 'client_credentials', 'scope': 'devices'})

    @patch('requests.request')
    def test_can_get_cached_token(self, request):
        request.return_value.json.return_value = self.token_response
        c = Client(**self.data)
        c.get_access_token()
        c.get_access_token()
        request.assert_called_once_with(
            'POST', 'http://localhost/oauth2/token',
            auth=(c.client, c.secret),
            data={'grant_type': 'client_credentials'})

    @patch('requests.request')
    def test_can_instrospect_token(self, request):
        request.return_value.json.return_value = self.token_response
        c = Client(**self.data)
        c.instrospect_token(self.token)
        headers = {'Authorization': 'bearer super-token'}
        data = {'token': 'super-token'}
        request.assert_called_with(
            'POST', 'http://localhost/oauth2/introspect',
            data=data, headers=headers)

    @patch('requests.request')
    def test_can_revoke_token(self, request):
        c = Client(**self.data)
        c.revoke_token(self.token)
        data = {'token': 'super-token'}
        request.assert_called_with(
            'POST', 'http://localhost/oauth2/revoke',
            data=data, auth=('client', 'secret'))
