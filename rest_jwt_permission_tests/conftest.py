# -*- coding: utf-8 -*-
def pytest_configure():
    from django.conf import settings

    MIDDLEWARE = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    )

    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        SITE_ID=1,
        SECRET_KEY='not very secret in tests',
        USE_I18N=True,
        USE_L10N=True,
        STATIC_URL='/static/',
        ROOT_URLCONF='rest_jwt_permission_tests.urls',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True
            },
        ],
        MIDDLEWARE=MIDDLEWARE,
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.staticfiles',
            'rest_framework',
            'rest_jwt_permission',
            'rest_jwt_permission_tests',
        ),
        PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.MD5PasswordHasher',
        ),
        AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
        ),
        JWT_AUTH = {
            "JWT_SECRET_KEY": "super-secret"
        },
        REST_FRAMEWORK = {
            "TEST_REQUEST_DEFAULT_FORMAT": 'json'
        }
    )

    try:
        import django
        django.setup()
    except AttributeError:
        pass
