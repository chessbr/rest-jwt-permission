# -*- coding: utf-8 -*-
import jwt
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header

from .settings import get_setting


def get_payload_from_scopes(scopes):
    """
    Get a dict to be used in JWT payload.
    Just merge this dict with the JWT payload.

    :type roles list[rest_jwt_permission.scopes.Scope]
    :return dictionary to be merged with the JWT payload
    :rtype dict
    """
    return {
        get_setting("JWT_PAYLOAD_SCOPES_KEY"): [scope.identifier for scope in scopes]
    }


def get_scopes_from_payload(payload):
    """
    Get a list of Scope from the JWT payload

    :type payload dict
    :rtype list[rest_jwt_permission.scopes.Scope]
    """
    return payload.get(get_setting("JWT_PAYLOAD_SCOPES_KEY"), [])


def get_jwt_payload_from_request(request):
    # lazy load this if one want to use other rest lib for JWT
    from rest_framework_jwt.settings import api_settings
    jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

    auth = get_authorization_header(request).split()
    auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()

    if not auth:
        if api_settings.JWT_AUTH_COOKIE:
            return request.COOKIES.get(api_settings.JWT_AUTH_COOKIE)
        return None

    if smart_text(auth[0].lower()) != auth_header_prefix:
        return None

    if len(auth) == 1:
        raise exceptions.PermissionDenied(_('No credentials provided.'))
    elif len(auth) > 2:
        raise exceptions.PermissionDenied(_('Invalid Authorization header.'))

    jwt_value = auth[1]
    if jwt_value is None:
        return None

    try:
        payload = jwt_decode_handler(jwt_value)
    except jwt.ExpiredSignature:
        raise exceptions.PermissionDenied(_('Signature has expired.'))
    except jwt.DecodeError:
        raise exceptions.PermissionDenied(_('Error decoding signature.'))
    except jwt.InvalidTokenError:
        raise exceptions.PermissionDenied(_('Invalid token.'))

    return payload
