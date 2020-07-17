import os
from ..utils.tar import find_tar_gz, untar
from ..utils.zip import find_zip, unzip

PLUGIN_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'plugins')
BASIC_APPS = [
    {
        'name': 'Asset',
        'icon': 'fa-cog',
        'component': '',
        'permission': 'asset.asset_view',

        'children': [
            {
                'name': 'Asset',
                'link': '',
                'permission': 'asset.asset_view',
            },
            {
                'name': 'Asset Group',
                'link': '',
                'permission': 'asset.asset_view',
            },
            {
                'name': 'System User',
                'permission': 'asset.asset_view',
                'link': ''
            },
            {
                'name': 'Permissions',
                'permission': 'asset.asset_view',
                'link': ''
            },
        ]
    },
    {
        'name': 'certificate',
        'icon': '',
    }
]

Plugins = []
PLUGINS_SETTING = []

for f in find_tar_gz(PLUGIN_PATH):
    try:
        untar(f, ".")
        os.remove(f)
    except Exception as e:
        raise e
for f in find_zip(PLUGIN_PATH):
    try:
        os.remove(f)
    except Exception as e:
        raise e

for f in os.listdir(PLUGIN_PATH):
    if os.path.isdir(os.path.join(PLUGIN_PATH, f)) and f != '__pycache__' \
        and os.path.isfile(os.path.join(PLUGIN_PATH, f, 'settings.py')):
        PLUGINS_SETTING.append(os.path.join(PLUGIN_PATH, f, 'settings.py'))

