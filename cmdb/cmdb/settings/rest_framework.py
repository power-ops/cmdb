# from .base import INSTALLED_APPS
INSTALLED_APPS += [
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    # 'snippets.apps.SnippetsConfig'
]
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'utils.authentication.AccessKeyAuthentication',
        # 'utils.authentication.AccessTokenAuthentication',
        # 'utils.authentication.PrivateTokenAuthentication',
        # 'utils.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}
