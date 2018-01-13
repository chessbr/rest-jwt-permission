# -*- coding: utf-8 -*-
from django.utils import module_loading
from django.utils.lru_cache import lru_cache

from rest_jwt_permission.settings import get_setting


@lru_cache()
def get_permission_providers():
    providers = []

    for provider in get_setting("SCOPE_PROVIDERS", []):
        provider_class = module_loading.import_string(provider)
        providers.append(provider_class())

    return providers
