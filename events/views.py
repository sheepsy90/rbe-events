from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render


def landing(request):
    if hasattr(request, 'user') and request.user.is_authenticated:
        return HttpResponseRedirect(settings.AFTER_LOGIN_URL)
    return render(request, 'events/landing.html')


@login_required(login_url=settings.LOGIN_URL)
def index(request):
    return render(request, 'events/index.html')


def meta(request):
    user_count = User.objects.all().count()
    return JsonResponse({'users': user_count})
