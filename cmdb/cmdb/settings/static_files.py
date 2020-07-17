import os
from .base import BASE_DIR

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/templates/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'templates')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'templates')
]
