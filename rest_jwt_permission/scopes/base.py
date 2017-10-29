# -*- coding: utf-8 -*-


class Scope(object):
    """
    A base scope.
    This indicates a permission access.
    The `identifier` should be unique.
    """
    identifier = None

    def __init__(self, identifier):
        self.identifier = identifier

    def get_description(self):
        return None

    def __str__(self):
        return "Base scope: {}".format(self.identifier)
