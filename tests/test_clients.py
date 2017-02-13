# Copyright (C) 2017 O.S. Systems Software LTDA.
# This software is released under the MIT License

import unittest

from hydra import Hydra, Client


class ClientsTestCase(unittest.TestCase):

    def setUp(self):
        self.hydra = Hydra('http://localhost:4444', 'client', 'secret')
        self.client = Client(
            name='new-client',
            secret='client-secret',
            scopes=['devices', 'products'],
            redirect_uris=['http://localhost/callback'],
        )

    def test_can_create_client(self):
        client = self.hydra.clients.create(self.client)
        self.addCleanup(self.hydra.clients.delete, client_id=client.id)
        self.assertEqual(client.name, 'new-client')
        self.assertEqual(client.secret, 'client-secret')
        self.assertEqual(client.scopes, ['devices', 'products'])
        self.assertEqual(client.redirect_uris, ['http://localhost/callback'])

    def test_can_get_client(self):
        client_id = self.hydra.clients.create(self.client).id
        self.addCleanup(self.hydra.clients.delete, client_id=client_id)
        client = self.hydra.clients.get(client_id)
        self.assertEqual(client.id, client_id)

    def test_can_update_client(self):
        client = self.hydra.clients.create(self.client)
        self.addCleanup(self.hydra.clients.delete, client_id=client.id)
        self.assertEqual(client.name, 'new-client')
        client.name = 'new-client-name'
        self.hydra.clients.update(client)
        self.assertEqual(client.name, 'new-client-name')

    def test_can_delete_client(self):
        client = self.hydra.clients.create(self.client)
        self.addCleanup(self.hydra.clients.delete, client_id=client.id)

        self.assertIsNotNone(self.hydra.clients.get(client.id))
        self.hydra.clients.delete(client.id)
        self.assertIsNone(self.hydra.clients.get(client.id))

    def test_can_list_all_clients(self):
        client1 = self.hydra.clients.create(self.client)
        self.addCleanup(self.hydra.clients.delete, client_id=client1.id)
        client2 = self.hydra.clients.create(self.client)
        self.addCleanup(self.hydra.clients.delete, client_id=client2.id)
        clients = [c.id for c in self.hydra.clients.all()]
        self.assertIn(client1.id, clients)
        self.assertIn(client2.id, clients)
