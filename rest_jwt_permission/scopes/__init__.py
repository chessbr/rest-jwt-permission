# -*- coding: utf-8 -*-
from .base import Scope
from .api import APIScope
from .simple import SimpleScope
from .utils import get_all_permission_providers_scopes


__all__ = [
    "APIScope",
    "Scope",
    "SimpleScope",
    "get_all_permission_providers_scopes"
]
