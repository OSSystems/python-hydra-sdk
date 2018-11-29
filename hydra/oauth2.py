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

    def reject_login_request(self, challenge, reject_login_config):
        response = self.request(
            'PUT', '/oauth2/auth/requests/login/{}/reject'.format(challenge),
            json=reject_login_config)
        if response.ok:
            return response.json()

    def reject_consent_request(self, challenge, reject_consent_config):
        response = self.request(
            'PUT', '/oauth2/auth/requests/consent/{}/reject'.format(challenge),
            json=reject_consent_config)
        if response.ok:
            return response.json()

    def revokes_all_previous_consent_session_user(self, user):
        response = self.request(
            'DELETE', '/oauth2/auth/sessions/consent/{}'
            .format(user))
        if response.ok:
            response.json()

    def revokes_consent_sessions_oAuth2_client(self, user, client):
        response = self.request(
            'DELETE', '/oauth2/auth/sessions/consent/{}/{}'
            .format(user, client))
        return response.ok

    def lists_all_consent_sessions_user(self, user):
        response = self.request(
            'GET', '/oauth2/auth/sessions/consent/{}' .format(user))
        if response.ok:
            return response.json()

    def logs_user_out_deleting_session_cookie(self):
        response = self.request(
            'GET', '/oauth2/auth/sessions/login/revoke')
        if response.ok:
            return response.json()

    def invalidates_users_authentication_session(self, user):
        response = self.request(
            'DELETE', '/oauth2/auth/sessions/login/{}' .format(user))
        print(response)
        if response.ok:
            return response

    def flush_expired_oAuth2_access_tokens(self, not_after):
        response = self.request(
            'POST', '/oauth2/flush', json=not_after)
        if response.ok:
            return response
