from cmdb.settings.view_settings import *  # import the settings file
from cmdb.settings.plugin import *
from django.contrib.auth.models import AnonymousUser


def settings(request):
    return {
        'settings': {
            'PROJECT_NAME': PROJECT_NAME,
            'BASIC_APPS': BASIC_APPS,
            'Plugins': Plugins
        },
    }
