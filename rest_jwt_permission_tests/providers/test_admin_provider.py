# -*- coding: utf-8 -*-
from django.test.utils import override_settings

from rest_jwt_permission.providers import get_permission_providers
from rest_jwt_permission.scopes import APIScope, Scope, SimpleScope, get_all_permission_providers_scopes


def setup_function():
    get_permission_providers.cache_clear()


def test_admin_scope_permission_provider():
    with override_settings(
        REST_JWT_PERMISSION={
            "SCOPE_PROVIDERS": [
                "rest_jwt_permission.providers.AdminScopeProvider"
            ]
        }
    ):
        scopes = get_all_permission_providers_scopes()
        expected_identifiers = [
            'superuser'
        ]
        scope_ids = [s.identifier for s in scopes]
        assert len(scope_ids) == len(expected_identifiers)
        assert set(scope_ids) == set(expected_identifiers)
        assert all([isinstance(s, Scope) for s in scopes])
        assert all([isinstance(s, SimpleScope) for s in scopes])
        assert not any([isinstance(s, APIScope) for s in scopes])
