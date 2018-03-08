[![Build Status](https://travis-ci.org/chessbr/rest-jwt-permission.svg?branch=master)](https://travis-ci.org/chessbr/rest-jwt-permission)
[![Coverage Status](https://coveralls.io/repos/github/chessbr/rest-jwt-permission/badge.svg?branch=master)](https://coveralls.io/github/chessbr/rest-jwt-permission?branch=master)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)


# Django Rest Framework JWT permissions

Module that check API View permissions from JWT payloads.

## Installation

```
pip install rest_jwt_permission
```

## Using

Add `rest_jwt_permission` in your `INSTALLED_APPS` and configure the `settings` as you wish. Here is an example:

```python
REST_JWT_PERMISSION = {
    "SCOPE_PROVIDERS": [
        "rest_jwt_permission.providers.APIEndpointScopeProvider",
        "rest_jwt_permission.providers.AdminScopeProvider"
    ],
    "GET_PAYLOAD_FROM_SCOPES_HANDLER": (
        "rest_jwt_permission.handlers.get_payload_from_scopes"
    ),
    "GET_SCOPES_FROM_PAYLOAD_HANDLER": (
        "rest_jwt_permission.handlers.get_scopes_from_payload"
    ),
    "GET_PAYLOAD_FROM_REQUEST_HANDLER": (
        "rest_jwt_permission.handlers.get_jwt_payload_from_request"
    )
}
```

Now you can use `JWTAPIPermission` class in your API Views through `permission_classes` property or even setting it as the default permission class in your [settings](http://www.django-rest-framework.org/api-guide/permissions/#setting-the-permission-policy)

### Example

For a more pratical example, check **[rest-jwt-permission-example](https://github.com/chessbr/rest-jwt-permission-example)**.

## Motivation

Inspired by GitHub [Personal access token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/) and by [Auth0 API Keys blog post](https://auth0.com/blog/using-json-web-tokens-as-api-keys/), this package provides a Django Rest Framework Permission object to check permissions from JWT payloads.

This enables your API to check permissions avoiding an extra database hit.

## How it works

Basically, it extracts a list of all Rest API Views and generate an unique ID for each endpoint + action. Then, after authenticaton, your API should inject which permission identifiers the user has access. The JWT payload should look like the following:

```json
{
  "scopes": [
    "myviewset:get"
    "function_endpoint:get",
    "basicview:get",
    "simpleviewsetpermission:custom_action:put",
    "modelviewsetpermission:retrieve:get",
    "modelviewsetpermission:destroy:delete",
    "modelviewsetpermission:some_detail_metod:patch",
  ]
}
```

On each authenticated request, the `JWTAPIPermission` permission class will generate the unique ID for the requested view and will check whether the JWT payloads contains the ID. If so, the user has access.

:warning: This package does not automatically injects the scopes payload into the JWT, although we have helpers (`rest_jwt_permission.handlers.get_payload_from_scopes`) you can use to do that. We strongly recommend you to use [REST framework JWT Auth](https://github.com/GetBlimp/django-rest-framework-jwt) package as it provides all you need to make this eaiser. You can change the payload handler though it's `JWT_PAYLOAD_HANDLER` setting.


You can also create some sort of admin page to select the permissions for user and/or groups like GitHub token scopes, and use that to inject the token into the JWT:

![GitHub Token Page](https://help.github.com/assets/images/help/settings/token_scopes.gif)


#### Scopes

Scopes are basically what users can access (has permission to do). Each scope should has an unique identifier (see [`Scope`](rest_jwt_permission/scopes/base.py) base class). You can extend the base `Scope` class and add extra properties and methods.


#### Providers

`Providers` are objects that returns a list of existing scopes. We currently have 2 built-in providers:

* `APIEndpointScopeProvider`: returns all scopes for Django REST Framework registered views.
* `AdminScopeProvider`: returns admin related scopes. Currently, only returns `superuser` scope.

You can develop new providers to your project as you need or even extend the built-ins.


### Settings

This project was build with extension in mind, so it is easy to extend, add or remove features.

See the list of settings you can customize, all of them are inside the `REST_JWT_PERMISSION` setting key:


**`SCOPE_PROVIDERS`**: List of providers used to extract the existing scopes.
Defaults to:
```
"SCOPE_PROVIDERS": [
    "rest_jwt_permission.providers.APIEndpointScopeProvider",
    "rest_jwt_permission.providers.AdminScopeProvider"
]
```

**`GET_PAYLOAD_FROM_SCOPES_HANDLER`**: Handler function to get the payload with scopes to be injected into JWT. Defaults to:
```
"GET_PAYLOAD_FROM_SCOPES_HANDLER": "rest_jwt_permission.handlers.get_payload_from_scopes"
```

**`GET_SCOPES_FROM_PAYLOAD_HANDLER`**: Handler function to get the scopes from a JWT payload. Defaults to:
```
"GET_SCOPES_FROM_PAYLOAD_HANDLER": "rest_jwt_permission.handlers.get_scopes_from_payload"
```

**`GET_PAYLOAD_FROM_REQUEST_HANDLER`**: Handler function to get JWT payload from Request. Defaults to:
```
"GET_PAYLOAD_FROM_REQUEST_HANDLER": "rest_jwt_permission.handlers.get_jwt_payload_from_request"
```

**`JWT_PAYLOAD_SCOPES_KEY`**: Payload key that will contain the scopes. Defaults to:
```
"JWT_PAYLOAD_SCOPES_KEY": "scopes"
```


### Showing all available roles

You can use the `show_roles` management command to print all available roles according to your providers.

```
python manage.py show_roles
```

## Running tests

Install dependencies from `dev-requirements.txt` and run `py.tets --cov`:

```
pip install dev-requirements.txt && py.tets --cov
```

# Compatibility

* Django >= 2.0
* Django Rest Framework >= 3.7

# License

MIT
