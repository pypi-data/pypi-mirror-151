# Built-in packages
import json
import pathlib

# Third-party packages
from faker import Faker
from pytest import mark as pt_mark
from pytest import param as pt_param
from pytest import raises as pt_raises
from pytest_mock import MockerFixture

# Local packages
from auth0_jwt_validator import JwtVerifier

from .utils import read_json

KEYS_PATH = pathlib.Path(__file__).parent / "keys"
PRIVATE_KEYS_FILEPATH = KEYS_PATH / "jwks-private.json"
PUBLIC_KEYS_FILEPATH = KEYS_PATH / "jwks-public.json"

fake = Faker()
private_keys = read_json(PRIVATE_KEYS_FILEPATH)
public_keys = read_json(PUBLIC_KEYS_FILEPATH)


issuer = f"https://{fake.domain_name()}"
jwks_uri = f"{issuer}/.well-known/jwks.json"
audience = f"{issuer}/api/v2"


@pt_mark.parametrize(
    ["auth0_jwks_uri", "issuer", "audience"],
    [pt_param(jwks_uri, issuer, audience, id="Auth0")],
)
def test_jwt_verifier_get_token_type(auth0_jwks_uri, issuer, audience):
    with pt_raises(NotImplementedError):
        jwt_verifier = JwtVerifier(auth0_jwks_uri, issuer, audience)
        jwt_verifier.get_token_type()


@pt_mark.parametrize(
    ["auth0_jwks_uri", "issuer", "audience"],
    [pt_param(jwks_uri, issuer, audience, id="Auth0")],
)
def test_jwt_verifier_verify_payload(auth0_jwks_uri, issuer, audience):
    with pt_raises(NotImplementedError):
        jwt_verifier = JwtVerifier(auth0_jwks_uri, issuer, audience)
        jwt_verifier.verify_payload({})


@pt_mark.parametrize(
    ["auth0_jwks_uri", "auth0_jwks_response", "issuer", "audience"],
    [pt_param(jwks_uri, public_keys, issuer, audience, id="Auth0")],
)
def test_jwt_verifier_verify(
    auth0_jwks_uri: str,
    auth0_jwks_response: str,
    issuer: str,
    audience: str,
    mocker: MockerFixture,
):

    jwt_verifier = JwtVerifier(auth0_jwks_uri, issuer, audience)

    mocker.patch.object(
        jwt_verifier, "get_auth0_signing_keys", lambda _: json.dumps(auth0_jwks_response)
    )

    payload = jwt_verifier.verify("")

    assert payload == {}
