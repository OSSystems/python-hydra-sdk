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
            'publichost': 'http://localhost:4444',
            'adminhost': 'http://localhost:4445',
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
        self.challenge = '0f4a657306bb476b9d95131d686d15ad'

    def test_can_create_client(self):
        c = Client(**self.data)
        self.assertEqual(c.publichost, 'http://localhost:4444')
        self.assertEqual(c.adminhost, 'http://localhost:4445')
        self.assertEqual(c.client, 'client')
        self.assertEqual(c.secret, 'secret')

    @patch('requests.request')
    def test_request_with_basic_authentication(self, request):
        c = Client(**self.data)
        c.request(
            'POST', '/oauth2/token', token=False, json={'token': 'foobar'})
        request.assert_called_with(
            'POST', 'http://localhost:4444/oauth2/token',
            auth=('client', 'secret'), json={'token': 'foobar'})

    @patch('requests.request')
    def test_request_with_token_authentication(self, request):
        request.return_value.json.return_value = self.token_response
        c = Client(**self.data)
        c.request('GET', '/clients', token=True)
        headers = {'Authorization': 'bearer super-token'}
        request.assert_called_with(
            'GET', 'http://localhost:4445/clients', headers=headers)

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
            'POST', 'http://localhost:4444/oauth2/token',
            auth=(c.client, c.secret),
            data={'grant_type': 'client_credentials'})

        c.get_access_token('devices')
        request.assert_called_with(
            'POST', 'http://localhost:4444/oauth2/token',
            auth=(c.client, c.secret),
            data={'grant_type': 'client_credentials', 'scope': 'devices'})

    @patch('requests.request')
    def test_can_get_cached_token(self, request):
        request.return_value.json.return_value = self.token_response
        c = Client(**self.data)
        c.get_access_token()
        c.get_access_token()
        request.assert_called_once_with(
            'POST', 'http://localhost:4444/oauth2/token',
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
            'POST', 'http://localhost:4445/oauth2/introspect',
            data=data, headers=headers)

    @patch('requests.request')
    def test_can_revoke_token(self, request):
        c = Client(**self.data)
        c.revoke_token(self.token)
        data = {'token': 'super-token'}
        request.assert_called_with(
            'POST', 'http://localhost:4444/oauth2/revoke',
            data=data, auth=('client', 'secret'))

    @patch('requests.request')
    def test_can_get_login_request(self, request):
        c = Client(**self.data)
        c.get_login_request(self.challenge)
        request.assert_called_with(
            'GET',
            'http://localhost:4445/oauth2/auth/requests/login/{}'
            .format(self.challenge),
            headers={'Authorization': 'None None'})

    @patch('requests.request')
    def test_can_accept_login_request(self, request):
        c = Client(**self.data)
        accept_config = {
            'remember_for': 0,
            'remember': False,
            'subject': c.client
        }
        c.accept_login_request(self.challenge, accept_config)
        request.assert_called_with(
            'PUT',
            'http://localhost:4445/oauth2/auth/requests/login/{}/accept'
            .format(self.challenge),
            headers={'Authorization': 'None None'},
            json=accept_config)

    @patch('requests.request')
    def test_can_get_consent_request(self, request):
        c = Client(**self.data)
        c.get_consent_request(self.challenge)
        request.assert_called_with(
            'GET',
            'http://localhost:4445/oauth2/auth/requests/consent/{}'
            .format(self.challenge),
            headers={'Authorization': 'None None'})

    @patch('requests.request')
    def test_can_accept_consent_request(self, request):
        c = Client(**self.data)
        accept_config = {
            'remember_for': 0,
            'remember': False,
            'session': {
                'access_token': self.token.ext
            },
        }
        c.accept_consent_request(self.challenge, accept_config)
        request.assert_called_with(
            'PUT',
            'http://localhost:4445/oauth2/auth/requests/consent/{}/accept'
            .format(self.challenge),
            headers={'Authorization': 'None None'},
            json=accept_config)
