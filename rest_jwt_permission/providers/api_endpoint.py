# -*- coding: utf-8 -*-
from django.utils.lru_cache import lru_cache
from rest_framework.schemas.generators import EndpointEnumerator

from rest_jwt_permission.utils import get_role_for, get_view_role

from .base import ScopeProviderBase


class APIEndpointScopeProvider(ScopeProviderBase):
    @lru_cache()
    def get_available_scopes(self):
        from rest_jwt_permission.scopes import APIScope

        epi = EndpointEnumerator()
        scopes = []

        for (path, method, callback) in epi.get_api_endpoints():
            view_class = callback.cls
            method = method.lower()
            action = callback.actions[method] if (hasattr(callback, "actions") and callback.actions) else None
            role = get_role_for(method, action)
            scope = get_view_role(view_class, role)
            scopes.append(APIScope(scope, path, method, view_class))

        return scopes
