# Copyright (C) 2017 O.S. Systems Software LTDA.
# This software is released under the MIT License

import os

import docker
import pytest


@pytest.fixture(scope='session', autouse=True)
def hydra_fixture():
    if os.environ.get('PYTHON_HYDRA_LOCAL'):
        yield
        return
    client = docker.from_env()
    env = {
        'FORCE_ROOT_CLIENT_CREDENTIALS': 'client:secret',
        'DATABASE_URL': 'memory',
    }
    ports = {'4444/tcp': 4444}
    entrypoint = '/go/bin/hydra host --dangerous-force-http'
    container = client.containers.run(
        'oryd/hydra:v0.9.16-http',
        detach=True,
        environment=env,
        ports=ports,
        entrypoint=entrypoint,
    )
    for line in container.logs(stream=True):
        if b'Setting up http server on :4444' in line:
            break
    yield
    container.kill()
    container.remove()
