# Copyright (C) 2017 O.S. Systems Software LTDA.
# This software is released under the MIT License

from datetime import datetime, timedelta

from jose import jwt

from .jwk import JWK


class Challenge:

    def __init__(self, hydra, challenge):
        self.hydra = hydra
        self.jwt = challenge
        self.data = self._decode()

    def _decode(self):
        jwk = self.hydra.jwk.get('hydra.consent.challenge', JWK.PUBLIC)
        key = {'keys': [jwk.jwk]}  # hack to bypass python-jose
        options = {'verify_aud': False}
        return jwt.decode(self.jwt, key, algorithms='RS256', options=options)

    def encode(self, sub, **kwargs):
        exp = int((datetime.utcnow() + timedelta(minutes=10)).timestamp())
        claims = {
            'sub': sub,
            'exp': exp,
            'iat': int(datetime.utcnow().timestamp()),
            'jti': self.data['jti'],
            'aud': self.data['aud'],
            'scp': self.data['scp'],
        }
        claims.update(kwargs)
        jwk = self.hydra.jwk.get('hydra.consent.response', JWK.PRIVATE)
        return jwt.encode(claims, jwk.to_rsa(), algorithm='RS256')
