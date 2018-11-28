# Copyright (C) 2017 O.S. Systems Software LTDA.
# This software is released under the MIT License

from datetime import datetime, timedelta
from urllib.parse import urljoin

import requests


class Token:

    def __init__(self, **kwargs):
        self.issue_time = datetime.now()
        self.expires_in = kwargs.get('expires_in', 0)
        self.scope = kwargs.get('scope')
        self.token = kwargs.get('access_token')
        self.type = kwargs.get('token_type')
        self.aud = kwargs.get('aud')
        self.client_id = kwargs.get('client_id')
        self.exp = kwargs.get('exp')
        self.ext = kwargs.get('exp')
        self.iat = kwargs.get('iat')
        self.iss = kwargs.get('iss')
        self.nbf = kwargs.get('nbf')
        self.obfuscated_subject = kwargs.get('obfuscated_subject')
        self.sub = kwargs.get('sub')
        self.username = kwargs.get('username')

    def is_expired(self):
        expiration_date = self.issue_time + timedelta(seconds=self.expires_in)
        return datetime.now() > expiration_date

    def __str__(self):
        return '{} {}'.format(self.type, self.token)


class Client:

    def __init__(self, publichost, adminhost, client, secret):
        self.publichost = publichost
        self.adminhost = adminhost
        self.client = client
        self.secret = secret
        self._tokens = {}

    def request(self, method, path, token=False, **kwargs):
        if token:
            url = urljoin(self.publichost, path)
            return self._token_request(method, url, **kwargs)
        url = urljoin(self.adminhost, path)
        return self._admin_request(method, url, **kwargs)

    def _admin_request(self, method, url, **kwargs):
        return requests.request(method, url, **kwargs)

    def _token_request(self, method, url, scope=None, **kwargs):
        kwargs['auth'] = (self.client, self.secret)
        return requests.request(method, url, **kwargs)

    def get_access_token(self, scope=None):
        token = self._tokens.get(scope)
        if token is not None and not token.is_expired():
            return token
        data = {'grant_type': 'client_credentials'}

        if scope is not None:
            data['scope'] = scope
        response = requests.request(
            'POST', urljoin(self.publichost, '/oauth2/token'),
            auth=(self.client, self.secret), data=data)
        if response.ok:
            token = Token(**response.json())
            self._tokens[scope] = token
            return token

    def instrospect_token(self, token):
        response = self.request(
            'POST', '/oauth2/introspect', data={'token': token.token})
        if response.ok:
            return response.json()

    def revoke_token(self, token):
        response = self.request(
            'POST', '/oauth2/revoke', token=True, data={'token': token.token})
        return response.ok

    def get_login_request(self, challenge):
        response = self.request(
            'GET', '/oauth2/auth/requests/login/{}'.format(challenge))
        if response.ok:
            return response.json()

    def get_consent_request(self, challenge):
        response = self.request(
            'GET', '/oauth2/auth/requests/consent/{}'.format(challenge))
        if response.ok:
            return response.json()

    def accept_login_request(self, challenge, accept_login_config):
        response = self.request(
            'PUT', '/oauth2/auth/requests/login/{}/accept'.format(challenge),
            json=accept_login_config)
        if response.ok:
            return response.json()

    def accept_consent_request(self, challenge, accept_consent_config):
        response = self.request(
            'PUT', '/oauth2/auth/requests/consent/{}/accept'.format(challenge),
            json=accept_consent_config)
        if response.ok:
            return response.json()
