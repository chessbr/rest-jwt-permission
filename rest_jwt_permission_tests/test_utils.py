# -*- coding: utf-8 -*-
from django.utils.text import slugify

from rest_jwt_permission.utils import get_role_for, get_view_id, get_view_role
from rest_jwt_permission_tests.factories import BasicView


def test_get_role_for():
    assert get_role_for("post", "save") == "save:post"
    assert get_role_for("POST", "Save") == "Save:post"
    assert get_role_for("get") == "get"
    assert get_role_for("PATCH") == "patch"


class ViewWithClassMethod(BasicView):
    @classmethod
    def get_view_permission_id(cls):
        return "MyViewID_InClassMethod"


class ViewWithInstanceMethod(BasicView):
    def get_view_permission_id(self):
        return "MyViewID_InstanceMethod"


class ViewWithAnything(object):
    pass


def test_get_view_id():
    assert get_view_id(BasicView) == slugify(BasicView.__name__)
    assert get_view_id(BasicView()) == slugify(BasicView.__name__)

    assert get_view_id(ViewWithClassMethod) == slugify("MyViewID_InClassMethod")
    assert get_view_id(ViewWithClassMethod()) == slugify("MyViewID_InClassMethod")
    assert get_view_id(ViewWithInstanceMethod) == slugify("MyViewID_InstanceMethod")
    assert get_view_id(ViewWithInstanceMethod()) == slugify("MyViewID_InstanceMethod")

    assert get_view_id(ViewWithAnything) == slugify(ViewWithAnything.__name__)
    assert get_view_id(ViewWithAnything()) == slugify(ViewWithAnything.__name__)


def test_get_view_role():
    assert get_view_role(BasicView, "method1") == "{}:{}".format(slugify(BasicView.__name__), "method1")
    assert get_view_role(BasicView(), "method2") == "{}:{}".format(slugify(BasicView.__name__), "method2")

    assert get_view_role(ViewWithClassMethod, "method3") == "{}:{}".format(slugify("MyViewID_InClassMethod"), "method3")
    assert get_view_role(ViewWithClassMethod(), "method4") == "{}:{}".format(slugify("MyViewID_InClassMethod"), "method4")
    assert get_view_role(ViewWithInstanceMethod, "method5") == "{}:{}".format(slugify("MyViewID_InstanceMethod"), "method5")
    assert get_view_role(ViewWithInstanceMethod(), "method6") == "{}:{}".format(slugify("MyViewID_InstanceMethod"), "method6")

    assert get_view_role(ViewWithAnything, "method9") == "{}:{}".format(slugify(ViewWithAnything.__name__), "method9")
    assert get_view_role(ViewWithAnything(), "method10") == "{}:{}".format(slugify(ViewWithAnything.__name__), "method10")
