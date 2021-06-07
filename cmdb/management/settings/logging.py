import os

LOG_ROOT = os.path.join(BASE_DIR, 'log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'daily': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, CONFIG.get('DJANGO', 'PROJECT_NAME', fallback='PLEASE_ADD_PROJECT_NAME')),
            'when': 'D',
            'backupCount': 20,
        },
    },
    'root': {
        'handlers': ['console', 'daily'],
        'level': 'DEBUG' if DEBUG else 'WARNING',
    },
}
