# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from rest_jwt_permission.scopes import get_all_permission_providers_scopes


class Command(BaseCommand):
    def handle(self, *args, **options):
        for x in get_all_permission_providers_scopes():
            print(x)
