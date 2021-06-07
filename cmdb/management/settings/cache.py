import os
from .base import DEBUG, CONFIG, BASE_DIR

if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': CONFIG.get('CACHE', 'PATH', fallback=os.path.join(BASE_DIR, 'cache')),
            'TIMEOUT': CONFIG.get('CACHE', 'TIMEOUT', fallback=60),  # 过期时间，单位为秒
            'OPTIONS': {
                'MAX_ENTRIES': CONFIG.get('CACHE', 'MAX_ENTRIES', fallback=1000)  # 最大缓存数，当缓存的数量超过后删除旧的缓存
            }
        }
    }
