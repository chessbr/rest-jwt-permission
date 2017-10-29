# -*- coding: utf-8 -*-
from django.utils import module_loading

REST_JWT_PERMISSION = {
    # List of scope  providers
    "SCOPE_PROVIDERS": [
        "rest_jwt_permission.providers.APIEndpointScopeProvider",
        "rest_jwt_permission.providers.AdminScopeProvider"
    ],

    # Handler function to get the payload with scopes to be injected in JWT payload
    "GET_PAYLOAD_FROM_SCOPES_HANDLER": (
        "rest_jwt_permission.handlers.get_payload_from_scopes"
    ),

    # Handler function to get the scopes from a JWT payload
    "GET_SCOPES_FROM_PAYLOAD_HANDLER": (
        "rest_jwt_permission.handlers.get_scopes_from_payload"
    ),

    # Handler function to get JWT payload from Request
    "GET_PAYLOAD_FROM_REQUEST_HANDLER": (
        "rest_jwt_permission.handlers.get_jwt_payload_from_request"
    ),

    # Payload key that will contain the scopes
    "JWT_PAYLOAD_SCOPES_KEY": "scopes"
}


def get_setting(setting_key, default=None):
    from django.conf import settings as django_settings
    settings = getattr(django_settings, "REST_JWT_PERMISSION", {})
    return settings.get(setting_key, REST_JWT_PERMISSION.get(setting_key, default))


def get_imported_setting(setting_key):
    return module_loading.import_string(get_setting(setting_key))
