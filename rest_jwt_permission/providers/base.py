# -*- coding: utf-8 -*-


class ScopeProviderBase(object):

    def get_available_scopes(self):
        """
        Returns a list of available Scope

        scope: is a string that uniquely identifies the permission level
        payload: additional content that might be serialized with format_payload()

        :rtype: list[rest_jwt_permission.Scope]
        """
        raise NotImplementedError()
