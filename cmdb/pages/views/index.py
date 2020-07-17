from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required


@login_required()
@require_http_methods(['GET'])
def ViewSet(request):
    return render(request, 'index.html')
