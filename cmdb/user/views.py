from django.shortcuts import render
from .models import User
from django.http import HttpResponseForbidden, HttpResponseRedirect
from .forms import SuperUserForm
from django.utils.translation import ugettext_lazy as _


def createsuperuser(request):
    _("Your password can’t be too similar to your other personal information.")
    _("Your password can’t be a commonly used password.")
    _("Your password can’t be entirely numeric.")
    if len(User.objects.filter(is_superuser=True)) == 0:
        if request.method == "GET":
            return render(request, 'createsuperuser.html', {'form': SuperUserForm()})
        elif request.method == "POST":
            form = SuperUserForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/login/')
            return render(request, 'createsuperuser.html', {'form': form})
    return HttpResponseForbidden()
