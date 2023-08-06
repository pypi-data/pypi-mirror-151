# Built-in packages
import json
import pathlib
import time

# Third-party packages
from faker import Faker
from pytest import mark as pt_mark
from pytest import param as pt_param
from pytest_mock import MockerFixture

# Local packages
from auth0_jwt_validator import (
    IdTokenVerifier,
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
subject = f"{fake.lexify(text='auth0|????')}"
audience = f"{issuer}/api/v2"
issued_at_time = int(time.time())
expiration_time = int(time.time() + 60)
authorized_party = f"{fake.word()}"
scope = "openid profile email"
permissions = ["create:user", "read:user", "update:user", "delete:user"]
grant_type = "client-credentials"
organization = f"{fake.word()}"
first_name = f"{fake.first_name_female()}"
last_name = f"{fake.last_name_female()}"
name = f"{first_name} {last_name}"
gender = "female"
birthdate = f"{fake.date_of_birth():%Y-%m-%d}"
email = f"{first_name.lower()}@{fake.free_email_domain()}"
picture = f"{fake.image_url()}"
nonce = f"{fake.lexify(text='????')}"
max_age = 60 * 60 * 24 * 30 * 12

# Missing issuer
jwt_payload_without_issuer = {
    "sub": subject,
    "aud": audience,
    "exp": expiration_time,
    "iat": issued_at_time,
    "name": name,
    "given_name": first_name,
    "family_name": last_name,
    "gender": gender,
    "birthdate": birthdate,
    "email": email,
    "picture": picture,
}
jwt_without_issuer = jwt.encode(
    {"alg": "RS256"}, jwt_payload_without_issuer, private_keys, check=False
)

# Wrong issuer
jwt_payload_with_wrong_issuer = {
    "iss": f"https://{fake.domain_name()}",
    "sub": subject,
    "aud": audience,
    "exp": expiration_time,
    "iat": issued_at_time,
    "name": name,
    "given_name": first_name,
    "family_name": last_name,
    "gender": gender,
    "birthdate": birthdate,
    "email": email,
    "picture": picture,
}
jwt_with_wrong_issuer = jwt.encode(
    {"alg": "RS256"}, jwt_payload_with_wrong_issuer, private_keys, check=False
)

# Missing subject
jwt_payload_without_subject = {
    "iss": issuer,
    "aud": audience,
    "exp": expiration_time,
    "iat": issued_at_time,
    "name": name,
    "given_name": first_name,
    "family_name": last_name,
    "gender": gender,
    "birthdate": birthdate,
    "email": email,
    "picture": picture,
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

# Missing nonce
jwt_payload_without_nonce = {
    "iss": issuer,
    "sub": subject,
    "aud": audience,
    "exp": expiration_time,
    "iat": issued_at_time,
    "name": name,
    "given_name": first_name,
    "family_name": last_name,
    "gender": gender,
    "birthdate": birthdate,
    "email": email,
    "picture": picture,
}
jwt_without_nonce = jwt.encode(
    {"alg": "RS256"}, jwt_payload_without_nonce, private_keys, check=False
)

# Wrong nonce
jwt_payload_with_wrong_nonce = {
    "iss": issuer,
    "sub": subject,
    "aud": audience,
    "exp": expiration_time,
    "iat": issued_at_time,
    "name": name,
    "given_name": first_name,
    "family_name": last_name,
    "gender": gender,
    "birthdate": birthdate,
    "email": email,
    "picture": picture,
    "nonce": f"{fake.lexify(text='?????')}",
}
jwt_with_wrong_nonce = jwt.encode(
    {"alg": "RS256"}, jwt_payload_with_wrong_nonce, private_keys, check=False
)

# With nonce
jwt_payload_with_nonce = {
    "iss": issuer,
    "sub": subject,
    "aud": audience,
    "exp": expiration_time,
    "iat": issued_at_time,
    "name": name,
    "given_name": first_name,
    "family_name": last_name,
    "gender": gender,
    "birthdate": birthdate,
    "email": email,
    "picture": picture,
    "nonce": nonce,
}
jwt_with_nonce = jwt.encode({"alg": "RS256"}, jwt_payload_with_nonce, private_keys, check=False)

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

# Missing authorized party
jwt_payload_without_authorized_party = {
    "iss": issuer,
    "sub": subject,
    "aud": [audience, f"https://{fake.domain_name()}/api/v2"],
    "exp": expiration_time,
    "iat": issued_at_time,
    "name": name,
    "given_name": first_name,
    "family_name": last_name,
    "gender": gender,
    "birthdate": birthdate,
    "email": email,
    "picture": picture,
}
jwt_without_authorized_party = jwt.encode(
    {"alg": "RS256"}, jwt_payload_without_authorized_party, private_keys, check=False
)

# Wrong authorized party
jwt_payload_with_wrong_authorized_party = {
    "iss": issuer,
    "sub": subject,
    "aud": [audience, f"https://{fake.domain_name()}/api/v2"],
    "exp": expiration_time,
    "iat": issued_at_time,
    "name": name,
    "given_name": first_name,
    "family_name": last_name,
    "gender": gender,
    "birthdate": birthdate,
    "email": email,
    "picture": picture,
    "azp": f"https://{fake.domain_name()}/api/v2",
}
jwt_with_wrong_authorized_party = jwt.encode(
    {"alg": "RS256"}, jwt_payload_with_wrong_authorized_party, private_keys, check=False
)

# With authorized party
jwt_payload_with_authorized_party = {
    "iss": issuer,
    "sub": subject,
    "aud": [audience, f"https://{fake.domain_name()}/api/v2"],
    "exp": expiration_time,
    "iat": issued_at_time,
    "name": name,
    "given_name": first_name,
    "family_name": last_name,
    "gender": gender,
    "birthdate": birthdate,
    "email": email,
    "picture": picture,
    "azp": audience,
}
jwt_with_authorized_party = jwt.encode(
    {"alg": "RS256"}, jwt_payload_with_authorized_party, private_keys, check=False
)

# Missing auth time
jwt_payload_without_auth_time = {
    "iss": issuer,
    "sub": subject,
    "aud": audience,
    "exp": expiration_time,
    "iat": issued_at_time,
    "name": name,
    "given_name": first_name,
    "family_name": last_name,
    "gender": gender,
    "birthdate": birthdate,
    "email": email,
    "picture": picture,
}
jwt_without_auth_time = jwt.encode(
    {"alg": "RS256"}, jwt_payload_without_auth_time, private_keys, check=False
)

# Expired auth time
jwt_payload_with_expired_auth_time = {
    "iss": issuer,
    "sub": subject,
    "aud": audience,
    "exp": expiration_time,
    "iat": issued_at_time,
    "name": name,
    "given_name": first_name,
    "family_name": last_name,
    "gender": gender,
    "birthdate": birthdate,
    "email": email,
    "picture": picture,
    "auth_time": int(time.time() - (60 * 60 * 24 * 30 * 12)),
}
jwt_with_expired_auth_time = jwt.encode(
    {"alg": "RS256"}, jwt_payload_with_expired_auth_time, private_keys, check=False
)

# Non-expired auth time
jwt_payload_with_nonexpired_auth_time = {
    "iss": issuer,
    "sub": subject,
    "aud": audience,
    "exp": expiration_time,
    "iat": issued_at_time,
    "name": name,
    "given_name": first_name,
    "family_name": last_name,
    "gender": gender,
    "birthdate": birthdate,
    "email": email,
    "picture": picture,
    "auth_time": int(time.time() + 60),
}
jwt_with_nonexpired_auth_time = jwt.encode(
    {"alg": "RS256"}, jwt_payload_with_nonexpired_auth_time, private_keys, check=False
)

# OK
jwt_payload_ok = {
    "iss": issuer,
    "sub": subject,
    "aud": audience,
    "exp": expiration_time,
    "iat": issued_at_time,
    "name": name,
    "given_name": first_name,
    "family_name": last_name,
    "gender": gender,
    "birthdate": birthdate,
    "email": email,
    "picture": picture,
}
jwt_ok = jwt.encode({"alg": "RS256"}, jwt_payload_ok, private_keys, check=False)


@pt_mark.parametrize(
    [
        "auth0_id_token",
        "auth0_organization",
        "nonce",
        "max_age",
        "id_token_verifier_verify_output",
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
            jwt_without_authorized_party,
            None,
            None,
            None,
            jwt_payload_without_authorized_party,
            id="Token without authorized party",
            marks=pt_mark.xfail(raises=MissingClaimError),
        ),
        pt_param(
            jwt_with_wrong_authorized_party,
            None,
            None,
            None,
            jwt_payload_with_wrong_authorized_party,
            id="Token with wrong authorized party",
            marks=pt_mark.xfail(raises=InvalidClaimError),
        ),
        pt_param(
            jwt_with_authorized_party,
            None,
            None,
            None,
            jwt_payload_with_authorized_party,
            id="Token with authorized party",
        ),
        pt_param(
            jwt_without_nonce,
            None,
            nonce,
            None,
            jwt_payload_without_nonce,
            id="Token without nonce",
            marks=pt_mark.xfail(raises=MissingClaimError),
        ),
        pt_param(
            jwt_with_wrong_nonce,
            None,
            nonce,
            None,
            jwt_payload_with_wrong_nonce,
            id="Token with wrong nonce",
            marks=pt_mark.xfail(raises=InvalidClaimError),
        ),
        pt_param(
            jwt_with_nonce,
            None,
            nonce,
            None,
            jwt_payload_with_nonce,
            id="Token with nonce",
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
            jwt_without_auth_time,
            None,
            None,
            max_age,
            jwt_payload_without_auth_time,
            id="Token without auth time",
            marks=pt_mark.xfail(raises=MissingClaimError),
        ),
        pt_param(
            jwt_with_expired_auth_time,
            None,
            None,
            max_age,
            jwt_payload_with_expired_auth_time,
            id="Token with expired auth time",
            marks=pt_mark.xfail(raises=InvalidClaimError),
        ),
        pt_param(
            jwt_with_nonexpired_auth_time,
            None,
            None,
            max_age,
            jwt_payload_with_nonexpired_auth_time,
            id="Token with non-expired auth time",
        ),
        pt_param(jwt_ok, None, None, None, jwt_payload_ok, id="Token OK"),
    ],
)
@pt_mark.parametrize(
    ["auth0_jwks_uri", "auth0_jwks_response", "issuer", "audience"],
    [pt_param(jwks_uri, public_keys, issuer, audience, id="Auth0")],
)
def test_id_token_verifier(
    auth0_jwks_uri: str,
    auth0_jwks_response: dict,
    issuer: str,
    audience: str,
    # cases
    auth0_id_token: str,
    auth0_organization: str,
    nonce,
    max_age,
    id_token_verifier_verify_output: dict,
    mocker: MockerFixture,
):
    token_verifier = IdTokenVerifier(auth0_jwks_uri, issuer, audience)

    mocker.patch.object(
        token_verifier,
        "get_auth0_signing_keys",
        lambda _: json.dumps(auth0_jwks_response),
    )

    payload = token_verifier.verify(
        auth0_id_token, nonce=nonce, max_age=max_age, organization=auth0_organization
    )

    assert payload == id_token_verifier_verify_output
