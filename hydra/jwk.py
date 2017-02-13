# Copyright (C) 2017 O.S. Systems Software LTDA.
# This software is released under the MIT License

import base64

from Crypto.PublicKey import RSA

from .base import HydraManager


class JWK:

    PUBLIC = 'public'
    PRIVATE = 'private'

    def __init__(self, **jwk):
        self.jwk = jwk
        self.kty = jwk.get('kty')
        self.alg = jwk.get('alg')
        self.kid = jwk.get('kid')

        self.n = jwk.get('n')
        self.e = jwk.get('e')
        self.d = jwk.get('d')

        self.type = None
        if all([self.n, self.e, self.d]):
            self.type = self.PRIVATE
        elif all([self.n, self.e]):
            self.type = self.PUBLIC

    @staticmethod
    def b64_to_int(data):
        return int.from_bytes(base64.urlsafe_b64decode(data + '=='), 'big')

    def to_rsa(self):
        """Converts a JWK to RSA."""
        numbers = [self.n, self.e]
        if self.type == self.PRIVATE:
            numbers.append(self.d)
        return RSA.construct(tuple(self.b64_to_int(n) for n in numbers))


class JWKManager(HydraManager):

    def get(self, key, type_):
        path = '/keys/{}/{}'.format(key, type_)
        response = self.hydra.request('GET', path, scope='hydra.keys.get')
        if response.ok:
            return JWK(**response.json()['keys'][0])
