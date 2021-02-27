from .base import CONFIG

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASE_DEFAULT = CONFIG.get('DJANGO', 'DATABASE_DEFAULT')
DATABASES = {
    'default': {
        'ENGINE': CONFIG.get('DATABASE:' + DATABASE_DEFAULT, 'ENGINE', fallback='django.db.backends.sqlite3'),
        'NAME': CONFIG.get('DATABASE:' + DATABASE_DEFAULT, 'NAME', fallback='db.sqlite3'),
        'USER': CONFIG.get('DATABASE:' + DATABASE_DEFAULT, 'USER', fallback=''),
        'PASSWORD': CONFIG.get('DATABASE:' + DATABASE_DEFAULT, 'PASSWORD', fallback=''),
        'HOST': CONFIG.get('DATABASE:' + DATABASE_DEFAULT, 'HOST', fallback=''),
        'PORT': CONFIG.get('DATABASE:' + DATABASE_DEFAULT, 'PORT', fallback=''),
    }
}
