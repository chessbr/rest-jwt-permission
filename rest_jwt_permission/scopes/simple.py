# -*- coding: utf-8 -*-
from .base import Scope


class SimpleScope(Scope):
    description = None

    def __init__(self, identifier, description):
        super(SimpleScope, self).__init__(identifier)
        self.description = description

    def get_description(self):
        return self.description

    def __str__(self):
        return "Simple scope: {}".format(self.identifier)
