# from .base import INSTALLED_APPS
INSTALLED_APPS += [
    'rest_framework',
    # 'rest_framework.authtoken',
    'drf_yasg',
    # 'snippets.apps.SnippetsConfig'
]
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}
SWAGGER_SETTINGS = {
    'LOGIN_URL': '/admin/login',
    'LOGOUT_URL': '/admin/logout',
    'PERSIST_AUTH': True,
    'REFETCH_SCHEMA_WITH_AUTH': True,
    'REFETCH_SCHEMA_ON_LOGOUT': True,

    'DEFAULT_INFO': 'DjangoDrfTest.urls.swagger_info',  # 这里注意，更改DjangoDrfTest

    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'authorization',
            'in': 'header'
        },
        'Query': {
            'type': 'apiKey',
            'name': 'auth',
            'in': 'query'
        }
    }
}
