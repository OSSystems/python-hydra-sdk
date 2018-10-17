# Copyright (C) 2017 O.S. Systems Software LTDA.
# This software is released under the MIT License

import os

import docker
import pytest
import tempfile
import shutil


@pytest.fixture(scope='session', autouse=True)
def hydra_fixture():
    if os.environ.get('PYTHON_HYDRA_LOCAL'):
        yield
        return

    client = docker.from_env()

    container_hydra_server = client.containers.run(
        'oryd/hydra:v1.0.0-beta.9',
        name='hydra_server',
        detach=True,
        environment={'DATABASE_URL': 'memory'},
        ports={'4444/tcp': 9000, '4445/tcp': 9001},
        command='serve all --dangerous-force-http',
        entrypoint='hydra',
        auto_remove=True
    )
    for line in container_hydra_server.logs(stream=True):
        if b'Setting up http server on :4444' in line:
            break

    container_add_client = client.containers.run(
        'oryd/hydra:v1.0.0-beta.9',
        environment={'HYDRA_ADMIN_URL': 'http://hydra:4445'},
        detach=True,
        links={'hydra_server': 'hydra'},
        command='clients create --skip-tls-verify '
        '--id client --secret secret '
        '--grant-types client_credentials,authorization_code '
        '--response-types token,code '
        '--scope hydra.keys.get,hydra.clients',
        auto_remove=True
    )
    for line in container_add_client.logs(stream=True):
        if b'OAuth2 client id: client' in line:
            container_add_client.kill()
            break
    yield

    container_hydra_server.kill()
