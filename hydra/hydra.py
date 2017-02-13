# Copyright (C) 2017 O.S. Systems Software LTDA.
# This software is released under the MIT License

from . import oauth2
from .clients import ClientManager
from .jwk import JWKManager


class Hydra(oauth2.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clients = ClientManager(self)
        self.jwk = JWKManager(self)
