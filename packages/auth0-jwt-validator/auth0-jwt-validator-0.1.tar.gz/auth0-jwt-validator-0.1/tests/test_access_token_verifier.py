# Built-in packages
import json
import pathlib
import time
import typing

# Third-party packages
from faker import Faker
from pytest import mark as pt_mark
from pytest import param as pt_param
from pytest_mock import MockerFixture

# Local packages
from auth0_jwt_validator import (
    AccessTokenVerifier,
    InvalidClaimError,
    MissingClaimError,
    jwt,
)

from .utils import read_json

KEYS_PATH = pathlib.Path(__file__).parent / "keys"
PRIVATE_KEYS_FILEPATH = KEYS_PATH / "jwks-private.json"
PUBLIC_KEYS_FILEPATH = KEYS_PATH / "jwks-public.json"


fake = Faker()
private_keys = read_json(PRIVATE_KEYS_FILEPATH)
public_keys = read_json(PUBLIC_KEYS_FILEPATH)


issuer = f"https://{fake.domain_name()}"
jwks_uri = f"{issuer}/.well-known/jwks.json"
subject = f"{fake.lexify(text='????????@????')}"
audience = f"{issuer}/api/v2"
issued_at_time = int(time.time())
expiration_time = int(time.time() + 60)
authorized_party = f"{fake.word()}"
scope = "openid profile email"
permissions = ["create:user", "read:user", "update:user", "delete:user"]
grant_type = "client-credentials"
organization = f"{fake.word()}"
required_scopes = scope.split()
required_permissions = [*permissions]

# Missing issuer
jwt_payload_without_issuer = {
    "sub": subject,
    "aud": audience,
    "iat": issued_at_time,
    "exp": expiration_time,
    "azp": authorized_party,
    "scope": scope,
    "gty": grant_type,
}
jwt_without_issuer = jwt.encode(
    {"alg": "RS256"}, jwt_payload_without_issuer, private_keys, check=False
)


# Wrong issuer
jwt_payload_with_wrong_issuer = {
    "iss": f"https://{fake.domain_name()}",
    "sub": subject,
    "aud": audience,
    "iat": issued_at_time,
    "exp": expiration_time,
    "azp": authorized_party,
    "scope": scope,
    "gty": grant_type,
}
jwt_with_wrong_issuer = jwt.encode(
    {"alg": "RS256"}, jwt_payload_with_wrong_issuer, private_keys, check=False
)


# Missing subject
jwt_payload_without_subject = {
    "iss": issuer,
    "aud": audience,
    "iat": issued_at_time,
    "exp": expiration_time,
    "azp": authorized_party,
    "scope": scope,
}
jwt_without_subject = jwt.encode(
    {"alg": "RS256"}, jwt_payload_without_subject, private_keys, check=False
)


# Missing audience
jwt_payload_without_audience = {
    "iss": issuer,
    "sub": subject,
    "iat": issued_at_time,
    "exp": expiration_time,
    "azp": authorized_party,
    "scope": scope,
}
jwt_without_audience = jwt.encode(
    {"alg": "RS256"}, jwt_payload_without_audience, private_keys, check=False
)


# Wrong audience not in audiences list
jwt_payload_with_wrong_audience_not_in_audiences_list = {
    "iss": issuer,
    "aud": [
        f"https://{fake.domain_name()}/api/v2",
        f"https://{fake.domain_name()}/api/v2",
    ],
    "sub": subject,
    "iat": issued_at_time,
    "exp": expiration_time,
    "azp": authorized_party,
    "scope": scope,
}
jwt_with_wrong_audience_not_in_audiences_list = jwt.encode(
    {"alg": "RS256"},
    jwt_payload_with_wrong_audience_not_in_audiences_list,
    private_keys,
    check=False,
)


# Wrong audience
jwt_payload_with_wrong_audience = {
    "iss": issuer,
    "aud": f"https://{fake.domain_name()}/api/v2",
    "sub": subject,
    "iat": issued_at_time,
    "exp": expiration_time,
    "azp": authorized_party,
    "scope": scope,
}
jwt_with_wrong_audience = jwt.encode(
    {"alg": "RS256"},
    jwt_payload_with_wrong_audience,
    private_keys,
    check=False,
)


# Missing issued at time
jwt_payload_without_issued_at_time = {
    "iss": issuer,
    "sub": subject,
    "aud": audience,
    "exp": expiration_time,
    "azp": authorized_party,
    "scope": scope,
}
jwt_without_issued_at_time = jwt.encode(
    {"alg": "RS256"}, jwt_payload_without_issued_at_time, private_keys, check=False
)


# Missing expiration time
jwt_payload_without_expiration_time = {
    "iss": issuer,
    "sub": subject,
    "aud": audience,
    "iat": issued_at_time,
    "azp": authorized_party,
    "scope": scope,
}
jwt_without_expiration_time = jwt.encode(
    {"alg": "RS256"}, jwt_payload_without_expiration_time, private_keys, check=False
)


# Expired expiration time
jwt_payload_with_expired_expiration_time = {
    "iss": issuer,
    "sub": subject,
    "aud": audience,
    "exp": int(time.time() - (60 * 60 * 24 * 30 * 12)),
    "iat": issued_at_time,
    "azp": authorized_party,
    "scope": scope,
}
jwt_with_expired_expiration_time = jwt.encode(
    {"alg": "RS256"},
    jwt_payload_with_expired_expiration_time,
    private_keys,
    check=False,
)


# Missing organization
jwt_payload_without_organization = {
    "iss": issuer,
    "sub": subject,
    "aud": audience,
    "iat": issued_at_time,
    "exp": expiration_time,
    "azp": authorized_party,
    "scope": scope,
}
jwt_without_organization = jwt.encode(
    {"alg": "RS256"}, jwt_payload_without_organization, private_keys, check=False
)


# Wrong organization
jwt_payload_with_wrong_organization = {
    "iss": issuer,
    "sub": subject,
    "aud": audience,
    "iat": issued_at_time,
    "exp": expiration_time,
    "azp": authorized_party,
    "scope": scope,
    "org_id": f"{fake.word()}",
}
jwt_with_wrong_organization = jwt.encode(
    {"alg": "RS256"}, jwt_payload_with_wrong_organization, private_keys, check=False
)


# Right organization
jwt_payload_with_organization = {
    "iss": issuer,
    "sub": subject,
    "aud": audience,
    "iat": issued_at_time,
    "exp": expiration_time,
    "azp": authorized_party,
    "scope": scope,
    "org_id": organization,
}
jwt_with_organization = jwt.encode(
    {"alg": "RS256"}, jwt_payload_with_organization, private_keys, check=False
)


# Without scope
jwt_payload_without_scope = {
    "iss": issuer,
    "sub": subject,
    "aud": audience,
    "iat": issued_at_time,
    "exp": expiration_time,
    "azp": authorized_party,
    "org_id": organization,
}
jwt_without_scope = jwt.encode(
    {"alg": "RS256"}, jwt_payload_without_scope, private_keys, check=False
)


# With wrong scope
jwt_payload_with_wrong_scope = {
    "iss": issuer,
    "sub": subject,
    "aud": audience,
    "iat": issued_at_time,
    "exp": expiration_time,
    "azp": authorized_party,
    "scope": f"{fake.word()}",
    "org_id": organization,
}
jwt_with_wrong_scope = jwt.encode(
    {"alg": "RS256"}, jwt_payload_with_wrong_scope, private_keys, check=False
)


# With scope
jwt_payload_with_scope = {
    "iss": issuer,
    "sub": subject,
    "aud": audience,
    "iat": issued_at_time,
    "exp": expiration_time,
    "azp": authorized_party,
    "scope": scope,
    "org_id": organization,
}
jwt_with_scope = jwt.encode({"alg": "RS256"}, jwt_payload_with_scope, private_keys, check=False)


# Without permissions
jwt_payload_without_permissions = {
    "iss": issuer,
    "sub": subject,
    "aud": audience,
    "iat": issued_at_time,
    "exp": expiration_time,
    "azp": authorized_party,
    "scope": scope,
    "org_id": organization,
}
jwt_without_permissions = jwt.encode(
    {"alg": "RS256"}, jwt_payload_without_permissions, private_keys, check=False
)


# With wrong permissions
jwt_payload_with_wrong_permissions = {
    "iss": issuer,
    "sub": subject,
    "aud": audience,
    "iat": issued_at_time,
    "exp": expiration_time,
    "azp": authorized_party,
    "scope": scope,
    "permissions": [
        f"create:{fake.job()}",
        f"read:{fake.job()}",
        f"update:{fake.job()}",
        f"delete:{fake.job()}",
    ],
    "org_id": organization,
}
jwt_with_wrong_permissions = jwt.encode(
    {"alg": "RS256"}, jwt_payload_with_wrong_permissions, private_keys, check=False
)


# With permissions
jwt_payload_with_permissions = {
    "iss": issuer,
    "sub": subject,
    "aud": audience,
    "iat": issued_at_time,
    "exp": expiration_time,
    "azp": authorized_party,
    "scope": scope,
    "permissions": permissions,
    "org_id": organization,
}
jwt_with_permissions = jwt.encode(
    {"alg": "RS256"}, jwt_payload_with_permissions, private_keys, check=False
)


# OK
jwt_payload_ok = {
    "iss": issuer,
    "sub": subject,
    "aud": audience,
    "iat": issued_at_time,
    "exp": expiration_time,
    "azp": authorized_party,
    "scope": scope,
    "org_id": organization,
}
jwt_ok = jwt.encode({"alg": "RS256"}, jwt_payload_ok, private_keys, check=False)


@pt_mark.parametrize(
    [
        "auth0_access_token",
        "auth0_organization",
        "required_scopes",
        "required_permissions",
        "access_token_verifier_verify_output",
    ],
    [
        pt_param(
            jwt_without_issuer,
            None,
            None,
            None,
            jwt_payload_without_issuer,
            id="Token without issuer",
            marks=pt_mark.xfail(raises=MissingClaimError),
        ),
        pt_param(
            jwt_with_wrong_issuer,
            None,
            None,
            None,
            jwt_payload_with_wrong_issuer,
            id="Token with wrong issuer",
            marks=pt_mark.xfail(raises=InvalidClaimError),
        ),
        pt_param(
            jwt_without_subject,
            None,
            None,
            None,
            jwt_payload_without_subject,
            id="Token without subject",
            marks=pt_mark.xfail(raises=MissingClaimError),
        ),
        pt_param(
            jwt_without_audience,
            None,
            None,
            None,
            jwt_payload_without_audience,
            id="Token without audience",
            marks=pt_mark.xfail(raises=MissingClaimError),
        ),
        pt_param(
            jwt_with_wrong_audience_not_in_audiences_list,
            None,
            None,
            None,
            jwt_payload_with_wrong_audience_not_in_audiences_list,
            id="Token with wrong audience not in audiences list",
            marks=pt_mark.xfail(raises=InvalidClaimError),
        ),
        pt_param(
            jwt_with_wrong_audience,
            None,
            None,
            None,
            jwt_payload_with_wrong_audience,
            id="Token with wrong audience",
            marks=pt_mark.xfail(raises=InvalidClaimError),
        ),
        pt_param(
            jwt_without_issued_at_time,
            None,
            None,
            None,
            jwt_payload_without_issued_at_time,
            id="Token without issued at time",
            marks=pt_mark.xfail(raises=MissingClaimError),
        ),
        pt_param(
            jwt_without_expiration_time,
            None,
            None,
            None,
            jwt_payload_without_expiration_time,
            id="Token without expiration time",
            marks=pt_mark.xfail(raises=MissingClaimError),
        ),
        pt_param(
            jwt_with_expired_expiration_time,
            None,
            None,
            None,
            jwt_payload_with_expired_expiration_time,
            id="Token with expired expiration time",
            marks=pt_mark.xfail(raises=InvalidClaimError),
        ),
        pt_param(
            jwt_without_organization,
            organization,
            None,
            None,
            jwt_payload_without_organization,
            id="Token without organization",
            marks=pt_mark.xfail(raises=MissingClaimError),
        ),
        pt_param(
            jwt_with_wrong_organization,
            organization,
            None,
            None,
            jwt_payload_with_wrong_organization,
            id="Token with wrong organization",
            marks=pt_mark.xfail(raises=InvalidClaimError),
        ),
        pt_param(
            jwt_with_organization,
            organization,
            None,
            None,
            jwt_payload_with_organization,
            id="Token with organization",
        ),
        pt_param(
            jwt_without_scope,
            None,
            required_scopes,
            None,
            jwt_payload_without_scope,
            id="Token without scope",
            marks=pt_mark.xfail(raises=MissingClaimError),
        ),
        pt_param(
            jwt_with_wrong_scope,
            None,
            required_scopes,
            None,
            jwt_payload_with_wrong_scope,
            id="Token with wrong scope",
            marks=pt_mark.xfail(raises=InvalidClaimError),
        ),
        pt_param(
            jwt_with_scope,
            None,
            required_scopes,
            None,
            jwt_payload_with_scope,
            id="Token with scope",
        ),
        pt_param(
            jwt_without_permissions,
            None,
            None,
            required_permissions,
            jwt_payload_without_permissions,
            id="Token without permissions",
            marks=pt_mark.xfail(raises=MissingClaimError),
        ),
        pt_param(
            jwt_with_wrong_permissions,
            None,
            None,
            required_permissions,
            jwt_payload_with_wrong_permissions,
            id="Token with wrong permissions",
            marks=pt_mark.xfail(raises=InvalidClaimError),
        ),
        pt_param(
            jwt_with_permissions,
            None,
            None,
            required_permissions,
            jwt_payload_with_permissions,
            id="Token wit permissions",
        ),
        pt_param(
            jwt_ok,
            None,
            None,
            None,
            jwt_payload_ok,
            id="Token OK",
        ),
    ],
)
@pt_mark.parametrize(
    ["auth0_jwks_uri", "auth0_jwks_response", "issuer", "audience"],
    [pt_param(jwks_uri, public_keys, issuer, audience, id="Auth0")],
)
def test_access_token_verifier(
    auth0_jwks_uri: str,
    auth0_jwks_response: dict,
    issuer: str,
    audience: str,
    # cases
    auth0_access_token: str,
    auth0_organization: typing.Optional[str],
    required_scopes: typing.Optional[typing.List[str]],
    required_permissions: typing.Optional[typing.List[str]],
    access_token_verifier_verify_output,
    mocker: MockerFixture,
):
    token_verifier = AccessTokenVerifier(auth0_jwks_uri, issuer, audience)

    mocker.patch.object(
        token_verifier,
        "get_auth0_signing_keys",
        lambda _: json.dumps(auth0_jwks_response),
    )

    payload = token_verifier.verify(
        auth0_access_token,
        organization=auth0_organization,
        required_scopes=required_scopes,
        required_permissions=required_permissions,
    )

    assert payload == access_token_verifier_verify_output
