# -*- coding: utf-8 -*-
from django.utils.lru_cache import lru_cache
from django.utils.translation import ugettext_lazy as _

from .base import ScopeProviderBase


class AdminScopeProvider(ScopeProviderBase):
    """
    Returns admin scopes
    """
    @lru_cache()
    def get_available_scopes(self):
        from rest_jwt_permission.scopes import SimpleScope
        return [
            SimpleScope("superuser", _("Super user access"))
        ]
