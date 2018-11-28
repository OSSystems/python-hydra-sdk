# Python Hydra SDK [![Build Status](https://travis-ci.org/OSSystems/python-hydra-sdk.svg?branch=master)](https://travis-ci.org/OSSystems/python-hydra-sdk) [![Coverage Status](https://coveralls.io/repos/github/OSSystems/python-hydra-sdk/badge.svg?branch=master)](https://coveralls.io/github/OSSystems/python-hydra-sdk?branch=master)

This package provides a Python SDK
for [Hydra](https://github.com/ory/hydra) OAuth2 and OpenID Connect
server made in Go.

## Installing

```
pip install hydra-sdk
```

## Basic usage

Documentation is still in progress...

```python
from hydra import Hydra

# First, create a Hydra client
hydra = Hydra(publichost='http://localhost:4444',adminhost='http://localhost:4445', client='client-server', secret='secret-server')

# Get an access token
token = hydra.get_access_token()

# Create a client
client = Client(
    name='new-client',
    secret='client-secret',
    scopes=['devices', 'products'],
    redirect_uris=['http://localhost/callback'],
)
client_id = hydra.clients.create(client).id

# Get a client
client = hydra.clients.get(cliente_id)
```

## Covered API

Hydra API coverage is a work in progress. You can check what is
already developed in the following list:

- Public Endpoints
  - [ ] JSON Web Keys Discovery
  - [ ] OpenID Connect Discovery
  - [ ] The OAuth 2.0 authorize endpoint
  - [x] Revoke OAuth2 tokens
  - [ ] The OAuth 2.0 token endpoint
  - [ ] OpenID Connect Userinfo
- Administrative Endpoints
  - [x] List OAuth 2.0 Clients
  - [x] Create an OAuth 2.0 client
  - [x] Get an OAuth 2.0 Client.
  - [x] Update an OAuth 2.0 Client
  - [x] Deletes an OAuth 2.0 Client
  - [ ] Retrieve a JSON Web Key Set
  - [ ] Update a JSON Web Key Set
  - [ ] Generate a new JSON Web Key
  - [ ] Delete a JSON Web Key Set
  - [ ] Fetch a JSON Web Key
  - [ ] Update a JSON Web Key
  - [ ] Delete a JSON Web Key
  - [x] Get consent request information
  - [x] Accept an consent request
  - [ ] Reject an consent request
  - [x] Get an login request
  - [x] Accept an login request
  - [ ] Reject a login request
  - [ ] Lists all consent sessions of a user
  - [ ] Revokes all previous consent sessions of a user
  - [ ] Revokes consent sessions of a user for a specific OAuth 2.0 Client
  - [ ] Logs user out by deleting the session cookie
  - [ ] Invalidates a user's authentication session
  - [ ] Flush Expired OAuth2 Access Tokens
  - [x] Introspect OAuth2 tokens

## License

Python Hydra SDK is released under MIT license.
