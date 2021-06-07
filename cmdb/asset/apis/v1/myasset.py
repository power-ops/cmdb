from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from management.utils import admin
from asset.models import Permission


@login_required()
@require_http_methods(['GET'])
@admin.has_permission('asset.view_asset')
def MyAssets(request):
    Assets = Permission.objects.UserAssets(request.user)
    Res = {}
    for asset, systemUsers in Assets.items():
        all_protocols = asset.Protocols.all()
        protocols = [p.uuid.__str__() for p in all_protocols]
        Res[asset.uuid.__str__()] = {
            'hostname': asset.Hostname,
            'ip': asset.IP,
            'protocols': protocols,
            'systemUsers': [{
                'id': su.uuid.__str__(),
                'name': su.__str__(),
                'username': su.Username,
                'protocol': [p.uuid.__str__() for p in list(su.Protocols.all().intersection(all_protocols))],
            } for su in systemUsers if list(su.Protocols.all().intersection(all_protocols))]
        }
    return JsonResponse(Res)
