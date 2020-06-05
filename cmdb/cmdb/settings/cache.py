from .base import DEBUG

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
            'LOCATION': '/tmp/cmdb.cache',
            'TIMEOUT': 60,  # 过期时间，单位为秒
            'OPTIONS': {
                'MAX_ENTRIES': 1000  # 最大缓存数，当缓存的数量超过后删除旧的缓存
            }
        }
    }
