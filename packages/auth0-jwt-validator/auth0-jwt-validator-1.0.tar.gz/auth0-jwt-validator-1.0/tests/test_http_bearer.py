# Built-in packages
import http
import typing

# Third-party packages
from pytest import mark as pt_mark
from pytest import param as pt_param

# Local packages
from auth0_jwt_validator import get_token


@pt_mark.parametrize(
    "authorization_header,expected_output",
    [
        pt_param(None, None, id="No authorization header"),
        pt_param("Token super-secret-token", None, id="Wrong authorization schema"),
        pt_param(
            "Bearer supe-secret-token extra-token", None, id="Wrong authorization bearer format"
        ),
        pt_param("Bearer", None, id="Missing bearer token"),
        pt_param(
            "Bearer super-secret-token",
            "super-secret-token",
            id="Right authorization bearer format",
        ),
    ],
)
def test_get_token(
    authorization_header: str,
    expected_output: typing.Tuple[
        typing.Optional[http.HTTPStatus], typing.Optional[str], typing.Optional[str]
    ],
):
    assert get_token(authorization_header) == expected_output
