# -*- coding: utf-8 -*-
import inspect

from django.utils.text import slugify


def get_role_for(method, action=None):
    if action:
        return "{}:{}".format(action, method.lower())
    return method.lower()


def get_view_id(view):
    view_class = None
    view_id = None

    if inspect.isclass(view):
        view_class = view
    else:
        view_class = view.__class__

    # check whether the view has the special get_view_permission_id classmethod
    if hasattr(view_class, "get_view_permission_id") and callable(view_class.get_view_permission_id):
        # check whether that is a class method
        if (inspect.ismethod(view_class.get_view_permission_id) and
                view_class.get_view_permission_id.__self__ is view_class):
            view_id = slugify(view_class.get_view_permission_id())
        else:
            view_id = slugify(view_class().get_view_permission_id())

    if not view_id:
        view_id = slugify(view_class.__name__)

    return view_id


def get_view_role(view, role):
    return "{}:{}".format(get_view_id(view), role)
