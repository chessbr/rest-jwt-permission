# -*- coding: utf-8 -*-
from rest_jwt_permission.scopes import APIScope, Scope, SimpleScope
from rest_jwt_permission_tests.factories import SimpleModelViewSet


def test_base_scope():
    assert Scope("ident1").identifier == "ident1"
    assert Scope("ident1").get_description() is None
    assert str(Scope("ident1")) == "Base scope: ident1"


def test_simple_scope():
    scope = SimpleScope("ident2", "my description")
    assert scope.identifier == "ident2"
    assert scope.get_description() == "my description"
    assert str(scope) == "Simple scope: ident2"


def test_api_scope():
    scope = APIScope("simple-api", "/path/action/", "post", SimpleModelViewSet)
    assert scope.identifier == "simple-api"
    assert scope.get_description() == "/path/action/"
    assert str(scope) == "API endpoint scope: simple-api - [POST]/path/action/ - SimpleModelViewSet"
