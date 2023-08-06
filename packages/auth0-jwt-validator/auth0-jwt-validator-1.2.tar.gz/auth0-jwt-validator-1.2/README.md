# Python Auth0 JWT Validator

[![Docs](https://github.com/immersa-co/python-auth0-jwt-validator/actions/workflows/docs.yml/badge.svg)](https://github.com/immersa-co/python-auth0-jwt-validator/actions/workflows/docs.yml)
[![Tests](https://github.com/immersa-co/python-auth0-jwt-validator/actions/workflows/tests.yml/badge.svg)](https://github.com/immersa-co/python-auth0-jwt-validator/actions/workflows/tests.yml)

---

**Documentation:** https://immersa-co.github.io/python-auth0-jwt-validator

**Source Code:** https://github.com/immersa-co/python-auth0-jwt-validator

---

# Getting Started

The package is framework agnostic, so we need to implement it on each framework
since each framework handles the requests and responses in different ways.

# Requirements

- Python 3.8+

# Installation

From PyPi

```
pip install auth0-jwt-validator
```

# Examples

## Flask Example

```python
from functools import wraps

from flask import Flask, request, jsonify
from auth0_jwt_validator import (
    get_token,
    AccessTokenVerifier,
    MissingClaimError,
    InvalidClaimError,
)

app = Flask(__name__)

auth0_jwks_uri = "https://<auth0-tenant>.us.auth0.com/.well-known/jwks.json"
issuer = "https://<auth0-tenant>.us.auth0.com/"
audience = "https://<auth0-tenant>.us.auth0.com/api/v2/"
access_token_verifier = AccessTokenVerifier(auth0_jwks_uri, issuer, audience)


@app.errorhandler(MissingClaimError)
def missing_claim_error_handler(e: MissingClaimError):
    return e.description, 401


@app.errorhandler(InvalidClaimError)
def missing_claim_error_handler(e: InvalidClaimError):
    return e.description, 401


def get_bearer_token(authorization: str | None) -> str | None:
    return get_token(authorization)


def get_access_token_payload(bearer_token: str | None) -> dict:
    return access_token_verifier.verify(bearer_token)


def route_get_access_token_payload(f):
    @wraps(f)
    def _route_get_access_token_payload(*args, **kwargs):
        authorization = request.headers.get("authorization")
        bearer_token = get_bearer_token(authorization)
        access_token_payload = get_access_token_payload(bearer_token)
        return f(*args, **kwargs, access_token_payload=access_token_payload)

    return _route_get_access_token_payload


@app.get("/")
@route_get_access_token_payload
def index(access_token_payload: dict):
    return jsonify({"access_token_payload": access_token_payload})
```

## Fast API Example

```python
from fastapi import FastAPI, Header, Request, HTTPException, Depends
from fastapi.exception_handlers import http_exception_handler
from auth0_jwt_validator import (
    get_token,
    AccessTokenVerifier,
    MissingClaimError,
    InvalidClaimError,
)

app = FastAPI()

auth0_jwks_uri = "https://<auth0-tenant>.us.auth0.com/.well-known/jwks.json"
issuer = "https://<auth0-tenant>.us.auth0.com/"
audience = "https://<auth0-tenant>.us.auth0.com/api/v2/"
access_token_verifier = AccessTokenVerifier(auth0_jwks_uri, issuer, audience)


@app.exception_handler(MissingClaimError)
def missing_claim_error_handler(request: Request, exc: MissingClaimError):
    return await http_exception_handler(
        request, HTTPException(status_code=401, detail=exc.description)
    )


@app.exception_handler(InvalidClaimError)
def missing_claim_error_handler(request: Request, exc: InvalidClaimError):
    return await http_exception_handler(
        request, HTTPException(status_code=401, detail=exc.description)
    )


async def get_bearer_token(
    authorization: str | None = Header(default=None),
) -> str | None:
    return get_token(authorization)


async def get_access_token_payload(
    bearer_token: str | None = Depends(get_bearer_token),
) -> dict:
    return access_token_verifier.verify(bearer_token)


@app.get("/")
async def index(access_token_payload: dict = Depends(get_access_token_payload)):
    return {"access_token_payload": access_token_payload}
```
