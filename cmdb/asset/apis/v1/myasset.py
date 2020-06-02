from asset.views import getMyAssets
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from utils import admin_permission as ap
from asset import admin


@login_required()
@require_http_methods(['GET'])
# @ap.has_view_permission(admin.AssetAdmin)
def MyAssets(request):
    Assets = getMyAssets(request)
    print(admin.AssetAdmin.has_view_permission(request=request))
    Res = {}
    for asset, systemUsers in Assets.items():
        protocols = list(set([p.Protocol for p in asset.Protocols.all()]))
        Res[asset.uuid.__str__()] = {
            'hostname': asset.Hostname,
            'ip': asset.IP,
            'protocols': protocols,
            'systemUsers': [{
                'id': su.uuid.__str__(),
                'name': su.__str__(),
                'username': su.Username,
                'protocol': su.Protocol,
            } for su in systemUsers if su.Protocol in protocols]
        }
    return JsonResponse(Res)
