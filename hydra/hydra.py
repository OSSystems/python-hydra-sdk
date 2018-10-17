# Copyright (C) 2017 O.S. Systems Software LTDA.
# This software is released under the MIT License

from datetime import datetime, timedelta
from . import oauth2
from .clients import ClientManager


class Hydra(oauth2.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clients = ClientManager(self)
