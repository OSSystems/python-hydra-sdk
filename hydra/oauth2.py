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

    def is_expired(self):
        expiration_date = self.issue_time + timedelta(seconds=self.expires_in)
        return datetime.now() > expiration_date

    def __str__(self):
        return '{} {}'.format(self.type, self.token)


class Client:

    def __init__(self, host, client, secret):
        self.host = host
        self.client = client
        self.secret = secret
        self._tokens = {}

    def request(self, method, path, token=True, **kwargs):
        url = urljoin(self.host, path)
        if token:
            return self._token_request(method, url, **kwargs)
        return self._basic_request(method, url, **kwargs)

    def _basic_request(self, method, url, **kwargs):
        kwargs['auth'] = (self.client, self.secret)
        return requests.request(method, url, **kwargs)

    def _token_request(self, method, url, scope=None, **kwargs):
        token = self.get_access_token(scope)
        headers = kwargs.setdefault('headers', {})
        headers['Authorization'] = str(token)
        return requests.request(method, url, **kwargs)

    def get_access_token(self, scope=None):
        token = self._tokens.get(scope)
        if token is not None and not token.is_expired():
            return token
        data = {'grant_type': 'client_credentials'}

        if scope is not None:
            data['scope'] = scope
        response = self.request(
            'POST', '/oauth2/token', token=False, data=data)
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
            'POST', '/oauth2/revoke', token=False, data={'token': token.token})
        return response.ok
