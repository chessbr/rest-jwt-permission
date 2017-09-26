# -*- coding: utf-8 -*-
import itertools

from rest_jwt_permission.providers import get_permission_providers


def get_all_permission_providers_scopes():
    providers_scopes = [provider.get_available_scopes() for provider in get_permission_providers()]
    return [scope for scope in itertools.chain(*providers_scopes)]
