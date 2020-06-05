from .base import config

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASE_DEFAULT = config.get('DJANGO', 'DATABASE_DEFAULT')
DATABASES = {
    'default': {
        'ENGINE': config.get('DATABASE:' + DATABASE_DEFAULT, 'ENGINE', fallback='django.db.backends.sqlite3'),
        'NAME': config.get('DATABASE:' + DATABASE_DEFAULT, 'NAME', fallback='db.sqlite3'),
        'USER': config.get('DATABASE:' + DATABASE_DEFAULT, 'USER', fallback=''),
        'PASSWORD': config.get('DATABASE:' + DATABASE_DEFAULT, 'PASSWORD', fallback=''),
        'HOST': config.get('DATABASE:' + DATABASE_DEFAULT, 'HOST', fallback=''),
        'PORT': config.get('DATABASE:' + DATABASE_DEFAULT, 'PORT', fallback=''),
    }
}
