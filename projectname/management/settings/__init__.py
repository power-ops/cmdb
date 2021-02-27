from split_settings.tools import optional, include

include(
    'base.py',
    'app.py',
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
