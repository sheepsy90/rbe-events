import datetime
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from events.models import Event


def landing(request):
    if hasattr(request, 'user') and request.user.is_authenticated:
        return HttpResponseRedirect(settings.AFTER_LOGIN_URL)
    return render(request, 'events/landing.html')


@login_required(login_url=settings.LOGIN_URL)
def index(request):
    todays_date = timezone.datetime.today().date()
    in_two_month_date = timezone.datetime.today().date() + datetime.timedelta(days=60)

    events = Event.objects.filter(begin_time__gte=todays_date, begin_time__lt=in_two_month_date).order_by('begin_time')
    context = {'events': events}
    return render(request, 'events/index.html', context)


def meta(request):
    user_count = User.objects.all().count()
    return JsonResponse({'users': user_count})


@login_required(login_url=settings.LOGIN_URL)
def create_event(request):
    return render(request, 'events/index.html')

@login_required(login_url=settings.LOGIN_URL)
def event_details(request, event_id):
    context = {}

    try:
        event = Event.objects.get(id=event_id)
        context['event'] = event
    except Event.DoesNotExist:
        pass
    return render(request, 'events/event_details.html', context)
