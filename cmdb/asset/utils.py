from django.db.models import Q
from asset.models import Permission
from django.core.cache import cache


def get_self_assets(request):
    if cache.get('getSelfAssets.' + request.user.username):
        return cache.get('getSelfAssets.' + request.user.username)
    assets = {}
    for res in Permission.objects.filter(
        Q(UserGroup__in=[g.id for g in request.user.groups.all()]) | Q(User=request.user.id)):
        system_user = [su for su in res.SystemUser.filter(Enabled=True).all()]
        for asset in res.Asset.filter(Enabled=True).all():
            if asset not in assets:
                assets[asset] = system_user
            else:
                assets[asset].extend(system_user)
        for assetGroup in res.AssetGroup.all():
            for asset in assetGroup.Assets.all():
                if asset not in assets:
                    assets[asset] = system_user
                else:
                    assets[asset].extend(system_user)
    for asset, system_user in assets.items():
        assets[asset] = list(set(system_user))
    cache.set('getSelfAssets.' + request.user.username, assets)
    return assets
