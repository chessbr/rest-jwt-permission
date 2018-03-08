# -*- coding: utf-8 -*-
import jwt
from django.utils.encoding import force_text

from rest_jwt_permission.handlers import get_jwt_payload_from_request, get_payload_from_scopes, get_scopes_from_payload
from rest_jwt_permission.scopes import SimpleScope


def test_get_payload_from_scopes_from_payload():
    scopes = [
        SimpleScope("scope-1", "desc1"),
        SimpleScope("scope-2", "desc2"),
        SimpleScope("scope-3", "desc3")
    ]

    payload = get_payload_from_scopes(scopes)
    assert payload == {"scopes": ["scope-1", "scope-2", "scope-3"]}

    payload.update({
        "add": "more",
        "stuff": "here",
        "garbage": [1, 2, 3, 4, 5]
    })

    assert get_scopes_from_payload(payload) == ["scope-1", "scope-2", "scope-3"]


def test_get_jwt_payload_from_request(rf):
    key = "super-secret"  # defined at conftest.py
    scopes = [
        SimpleScope("scope-1", "desc1"),
        SimpleScope("scope-2", "desc2"),
        SimpleScope("scope-3", "desc3")
    ]
    payload = get_payload_from_scopes(scopes)
    encoded = jwt.encode(payload, key, algorithm='HS256')

    request = rf.post("/", HTTP_AUTHORIZATION="JWT {}".format(force_text(encoded)))
    request_payload = get_jwt_payload_from_request(request)
    assert payload == request_payload
