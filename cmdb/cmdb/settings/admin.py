INSTALLED_APPS += [
    'admin_reorder',
]
ADMIN_REORDER = [
    {'app': 'auth', 'models': ('user.User', 'user.Group', 'authtoken.Token')},
    {'app': 'asset', 'models': (
        'asset.Asset', 'asset.AssetGroup',
        'asset.Label', 'asset.Platform', 'asset.Protocol',
        'asset.SystemUser',
        'asset.Permission')},
    {'app': 'domain', 'models': ('domain.Domain', 'domain.DNSRecord', 'domain.Certificate')},
    {'app': 'service', 'models': ('service.Service',)},
    {'app': 'audits', 'models': ('audits.ApiLog', 'audits.AssetLogin',)},
]
