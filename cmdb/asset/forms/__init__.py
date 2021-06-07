try:  # 增加try的原因是form里有queryset，会导致makemigration失败
    from .asset import AssetForm
    from .systemuser import SystemUserForm
    from .perms import PermsForm
    from .asset_group import AssetGroupForm
except:
    pass
