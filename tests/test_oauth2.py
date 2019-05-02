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
            'POST', '/oauth2/token', token=False,
            auth=('client', 'secret'), json={'token': 'foobar'})
        request.assert_called_with(
            'POST', 'http://localhost:4445/oauth2/token',
            auth=('client', 'secret'), json={'token': 'foobar'})

    @patch('requests.request')
    def test_request_with_token_authentication(self, request):
        request.return_value.json.return_value = self.token_response
        c = Client(**self.data)
        c.request('GET', '/clients', token=True)
        auth = ('client', 'secret')
        request.assert_called_with(
            'GET', 'http://localhost:4444/clients', auth=auth)

    @patch('requests.request')
    def test_can_instrospect_token(self, request):
        request.return_value.json.return_value = self.token_response
        c = Client(**self.data)
        c.instrospect_token(self.token)
        data = {'token': 'super-token'}
        request.assert_called_with(
            'POST', 'http://localhost:4445/oauth2/introspect',
            data=data)

    @patch('requests.request')
    def test_can_revoke_token(self, request):
        c = Client(**self.data)
        c.revoke_token(self.token)
        data = {'token': 'super-token'}
        auth = ('client', 'secret')
        request.assert_called_with(
            'POST', 'http://localhost:4444/oauth2/revoke',
            data=data, auth=auth)

    @patch('requests.request')
    def test_can_get_login_request(self, request):
        c = Client(**self.data)
        c.get_login_request(self.challenge)
        request.assert_called_with(
            'GET',
            'http://localhost:4445/oauth2/auth/requests/login',
            params={'login_challenge': self.challenge})

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
            'http://localhost:4445/oauth2/auth/requests/login/accept',
            params={'login_challenge': self.challenge},
            json=accept_config)

    @patch('requests.request')
    def test_can_get_consent_request(self, request):
        c = Client(**self.data)
        c.get_consent_request(self.challenge)
        request.assert_called_with(
            'GET',
            'http://localhost:4445/oauth2/auth/requests/consent',
            params={'consent_challenge': self.challenge})

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
            'http://localhost:4445/oauth2/auth/requests/consent/accept',
            params={'consent_challenge': self.challenge},
            json=accept_config)

    @patch('requests.request')
    def test_can_reject_login_request(self, request):
        c = Client(**self.data)
        reject_config = {
            'error': 'test',
            'error_debug': 'test',
            'error_description': 'test',
            'error_hint': 'test',
            'status_code': 404
        }
        c.reject_login_request(self.challenge, reject_config)
        request.assert_called_once_with(
            'PUT',
            'http://localhost:4445/oauth2/auth/requests/login/reject',
            params={'login_challenge': self.challenge},
            json=reject_config)

    @patch('requests.request')
    def test_can_reject_consent_request(self, request):
        c = Client(**self.data)
        reject_config = {
            'error': 'test',
            'error_debug': 'test',
            'error_description': 'test',
            'error_hint': 'test',
            'status_code': 404
        }
        c.reject_consent_request(self.challenge, reject_config)
        request.assert_called_once_with(
            'PUT',
            'http://localhost:4445/oauth2/auth/requests/consent/reject',
            params={'consent_challenge': self.challenge},
            json=reject_config)

    @patch('requests.request')
    def test_can_revokes_all_previous_consent_session_user(self, request):
        c = Client(**self.data)
        user = 'user'
        c.revokes_all_previous_consent_session_user(user)
        request.assert_called_once_with(
            'DELETE',
            'http://localhost:4445/oauth2/auth/sessions/consent',
            params={'subject': user}
        )

    @patch('requests.request')
    def test_can_revoke_consent_sessions_oAuth2_client(self, request):
        c = Client(**self.data)
        user = 'user'
        client = c.client
        c.revokes_consent_sessions_oAuth2_client(user, c.client)
        request.assert_called_with(
            'DELETE',
            'http://localhost:4445/oauth2/auth/sessions/consent',
            params={'subject': user, 'client': client})

    @patch('requests.request')
    def test_can_lists_all_consent_sessions_user(self, request):
        c = Client(**self.data)
        user = 'user'
        c.lists_all_consent_sessions_user(user)
        request.assert_called_once_with(
            'GET',
            'http://localhost:4445/oauth2/auth/sessions/consent',
            params={'subject': user})

    @patch('requests.request')
    def test_can_logs_user_out_deleting_session_cookie(self, request):
        c = Client(**self.data)
        c.logs_user_out_deleting_session_cookie()
        request.assert_called_once_with(
            'GET',
            'http://localhost:4445/oauth2/auth/sessions/login/revoke')
