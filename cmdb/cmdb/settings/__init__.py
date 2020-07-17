from split_settings.tools import optional, include
from .plugin import PLUGIN_PATH, PLUGINS_SETTING

include(
    'base.py',
    'database.py',
    '*.py',
    #     # the project different envs settings
    #     optional('envs/devel/*.py'),
    #     optional('envs/production/*.py'),
    #     optional('envs/staging/*.py'),
    #
    #     # for any local settings
    #     optional(‘local_settings.py
    # '),
)
for setting in PLUGINS_SETTING:
    include(setting)
