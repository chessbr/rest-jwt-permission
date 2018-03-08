# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.test.utils import override_settings
from rest_framework import routers

from rest_jwt_permission.providers import get_permission_providers
from rest_jwt_permission.scopes import APIScope, Scope, SimpleScope, get_all_permission_providers_scopes
from rest_jwt_permission_tests.factories import BasicView, SimpleModelViewSet, SimpleViewSet, function_endpoint


def setup_function(fn):
    get_permission_providers.cache_clear()


router = routers.DefaultRouter()
router.register(r'simple-viewset', SimpleViewSet)
router.register(r'model-viewset', SimpleModelViewSet)

urlpatterns = [
    url(r'^simple/$', BasicView.as_view()),
    url(r'^function/$', function_endpoint),
    url(r'^', include(router.urls)),
]


def test_api_endpoint_scope_permission_provider():
    with override_settings(
        ROOT_URLCONF="rest_jwt_permission_tests.providers.test_api_endpoint_provider",
        REST_JWT_PERMISSION={
            "SCOPE_PROVIDERS": [
                "rest_jwt_permission.providers.APIEndpointScopeProvider"
            ]
        }
    ):
        scopes = get_all_permission_providers_scopes()
        expected_identifiers = [
            'function_endpoint:get',
            'function_endpoint:post',
            'simplemodelviewset:list:get',
            'simplemodelviewset:create:post',
            'simplemodelviewset:some_method:get',
            'simplemodelviewset:some_method:delete',
            'simplemodelviewset:retrieve:get',
            'simplemodelviewset:update:put',
            'simplemodelviewset:partial_update:patch',
            'simplemodelviewset:destroy:delete',
            'simplemodelviewset:some_detail_metod:get',
            'simplemodelviewset:some_detail_metod:post',
            'simplemodelviewset:some_detail_metod:put',
            'simplemodelviewset:some_detail_metod:patch',
            'simpleviewset:patch_put:put',
            'simpleviewset:patch_put:patch',
            'basicview:get',
            'basicview:post'
        ]
        scope_ids = [s.identifier for s in scopes]
        assert len(scope_ids) == len(expected_identifiers)
        assert set(scope_ids) == set(expected_identifiers)
        assert all([isinstance(s, Scope) for s in scopes])
        assert all([isinstance(s, APIScope) for s in scopes])
        assert not any([isinstance(s, SimpleScope) for s in scopes])
