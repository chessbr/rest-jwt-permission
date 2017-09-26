# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission

from .settings import get_imported_setting
from .utils import get_role_for, get_view_role


class JWTAPIPermission(BasePermission):
    """
    Returns whether the scope is inside the JWT payload
    """
    def has_permission(self, request, view):
        get_jwt_payload_from_request = get_imported_setting("GET_PAYLOAD_FROM_REQUEST_HANDLER")
        get_scopes_from_payload = get_imported_setting("GET_SCOPES_FROM_PAYLOAD_HANDLER")

        payload = get_jwt_payload_from_request(request)

        if not payload:
            return False

        payload_scopes = get_scopes_from_payload(payload)
        role = get_role_for(request.method.lower(), getattr(view, "action", None))
        scope = get_view_role(view, role)

        return scope in payload_scopes
