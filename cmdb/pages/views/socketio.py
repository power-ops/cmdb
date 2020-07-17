from django.shortcuts import render


def ViewSet(request):
    return render(request, 'socketio.html')
