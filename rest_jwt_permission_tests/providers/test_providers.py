# -*- coding: utf-8 -*-
import pytest
from django.test.utils import override_settings

from rest_jwt_permission.providers import (
    AdminScopeProvider, APIEndpointScopeProvider, get_permission_providers
)
from rest_jwt_permission.providers.base import ScopeProviderBase


def setup_function(fn):
    get_permission_providers.cache_clear()


def test_base_provider():
    with pytest.raises(NotImplementedError):
        ScopeProviderBase().get_available_scopes()


def test_get_permission_providers():
    # default providers
    providers = get_permission_providers()
    assert len(providers) == 2
    assert AdminScopeProvider in [provider.__class__ for provider in providers]
    assert APIEndpointScopeProvider in [provider.__class__ for provider in providers]

    # clear the lru_cache
    get_permission_providers.cache_clear()

    with override_settings(REST_JWT_PERMISSION={
        "SCOPE_PROVIDERS": [
            "rest_jwt_permission.providers.APIEndpointScopeProvider"
        ]
    }):
        providers = get_permission_providers()
        assert len(providers) == 1
        assert providers[0].__class__ == APIEndpointScopeProvider

    # clear the lru_cache
    get_permission_providers.cache_clear()

    with override_settings(REST_JWT_PERMISSION={
        "SCOPE_PROVIDERS": [
            "rest_jwt_permission.providers.AdminScopeProvider"
        ]
    }):
        providers = get_permission_providers()
        assert len(providers) == 1
        assert providers[0].__class__ == AdminScopeProvider
