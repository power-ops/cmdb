try:  # 增加try的原因是form里有queryset，会导致makemigration失败
    from .asset import AssetAdmin
    from .protocol import ProtocolAdmin
    from .systemuser import SystemUserAdmin
    from .asset_group import AssteGroupAdmin
    from .label import LabelAdmin
    from .perms import PermsAdmin
    from .platform import PlatformAdmin
except:
    pass
