import os
from .base import BASE_DIR

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale'), ]

LANGUAGES = (
    ('zh-hans', '简体中文'),
    ('en', 'English')
)
LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True
