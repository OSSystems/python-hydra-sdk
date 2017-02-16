# Copyright (C) 2017 O.S. Systems Software LTDA.
# This software is released under the MIT License

from datetime import datetime, timedelta

from jose import jwt as jose_jwt

from . import oauth2
from .clients import ClientManager
from .jwk import JWK, JWKManager


class Hydra(oauth2.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clients = ClientManager(self)
        self.jwk = JWKManager(self)

    def challenge_decode(self, jwt):
        jwk = self.jwk.get('hydra.consent.challenge', JWK.PUBLIC)
        key = {'keys': [jwk.jwk]}  # hack to bypass python-jose
        options = {'verify_aud': False}
        return jose_jwt.decode(jwt, key, algorithms='RS256', options=options)

    def challenge_encode(self, challenge, sub, **kwargs):
        exp = int((datetime.utcnow() + timedelta(minutes=10)).timestamp())
        claims = {
            'sub': sub,
            'exp': exp,
            'iat': int(datetime.utcnow().timestamp()),
            'jti': challenge['jti'],
            'aud': challenge['aud'],
            'scp': challenge['scp'],
        }
        claims.update(kwargs)
        jwk = self.jwk.get('hydra.consent.response', JWK.PRIVATE)
        return jose_jwt.encode(claims, jwk.to_rsa(), algorithm='RS256')
