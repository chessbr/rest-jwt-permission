# -*- coding: utf-8 -*-
from .base import Scope


class APIScope(Scope):
    path = None
    method = None
    view_class = None

    def __init__(self, identifier, path, method, view_class):
        super(APIScope, self).__init__(identifier)
        self.path = path
        self.method = method
        self.view_class = view_class

    def get_description(self):
        return self.path

    def __str__(self):
        return "API endpoint scope: {} - [{}]{} - {}".format(
            self.identifier, self.method.upper(), self.path, self.view_class.__name__
        )
