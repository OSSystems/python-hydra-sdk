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
hydra = Hydra(host='http://localhost:4444', client='client_id', secret='client_secret')

# Get an access token
token = hydra.get_access_token(scope=['hydra'])

# Get a client
client = hydra.clients.get('admin')
```

## Covered API

Hydra API coverage is a work in progress. You can check what is
already developed in the following list:

- OAuth2
  - [x] Get access token (with token cache)
  - [x] Introspect token
  - [x] Revoke token
- Login
  - [x] Get login challenge
  - [x] Accept login challenge
- Consent
  - [x] Get consent challenge
  - [x] Accept consent response
- Clients
  - [x] Create new client
  - [x] Retrieve client information
  - [x] List all clients
  - [x] Update client
  - [x] Delete client
- Policies
  - [ ] Create new policy
  - [ ] Retrieve policy details
  - [ ] Find policy by subject
  - [ ] Delete policy
- Warden
  - [ ] Token access control
  - [ ] Subject access control

## License

Python Hydra SDK is released under MIT license.
