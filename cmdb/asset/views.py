from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from asset.models import Permission
from django.core.cache import cache


@login_required()
@require_http_methods(['GET'])
def MyAssetsView(request):
    return render(request, 'myassets.html', {"Assets": getSelfAssets(request)})


def getSelfAssets(request):
    if cache.get('getSelfAssets_' + request.user.username):
        return cache.get('getSelfAssets_' + request.user.username)
    Assets = {}
    for res in Permission.objects.filter(
            Q(UserGroup__in=[g.id for g in request.user.groups.all()]) | Q(User=request.user.id)):
        systemUser = [su for su in res.SystemUser.filter(Enabled=True).all()]
        for asset in res.Asset.filter(Enabled=True).all():
            if asset not in Assets:
                Assets[asset] = systemUser
            else:
                Assets[asset].extend(systemUser)
        for assetGroup in res.AssetGroup.all():
            for asset in assetGroup.Assets.all():
                if asset not in Assets:
                    Assets[asset] = systemUser
                else:
                    Assets[asset].extend(systemUser)
    for asset, systemUser in Assets.items():
        Assets[asset] = list(set(systemUser))
    cache.set('getSelfAssets_' + request.user.username, Assets)
    return Assets
