from .base import CONFIG

AUTH_USER_MODEL = 'user.User'
AVATAR = CONFIG.get('POWER_OPS', 'AVATAR_PATH', fallback='/opt/cmdb/avatar/')
