# Python Hydra SDK

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
- Consent
  - [x] Decode consent challenge
  - [x] Encode consent response
- Clients
  - [x] Create new client
  - [x] Retrieve client information
  - [x] List all clients
  - [x] Update client
  - [x] Delete client
- JWK
  - [ ] Get JWK set
  - [ ] Generate JWK set
  - [ ] Upload JWK set
  - [ ] Delete JWK set
  - [x] Get JWK key
  - [ ] Set JWK key
  - [ ] Delete JWK key
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
