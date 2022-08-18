from graphql_jwt.utils import get_user_by_payload
from graphql_jwt.utils import jwt_decode as graphql_jwt_decode
from graphql_jwt.utils import jwt_payload as graphql_jwt_payload
from jwt import MissingRequiredClaimError, InvalidTokenError


class InvalidJwtIdError(InvalidTokenError):
    pass


def jwt_payload(user, context=None):
    payload = graphql_jwt_payload(user, context)
    payload["jti"] = user.jti
    print(payload.get('jti'))
    return payload


def jwt_decode(token, context=None):
    payload = graphql_jwt_decode(token, context)
    user = get_user_by_payload(payload)
    validate_jti(payload, user)
    return payload


def validate_jti(payload, user):
    if not user.is_authenticated:
        return
    if user.jti is None:
        return
    if "jti" not in payload:
        raise MissingRequiredClaimError("jti")
    if payload["jti"] != user.jti:
        raise InvalidJwtIdError("Invalid Token")
