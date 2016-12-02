import datetime
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from events.forms import EventForm
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
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EventForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            print request.user
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            language = form.cleaned_data['language']
            medium = form.cleaned_data['medium']
            begin_time = form.start_datetime
            end_time = form.end_datetime

            event = Event(creator=request.user, title=title, description=description, begin_time=begin_time,
                          end_time=end_time, language=language, medium=medium)

            event.save()

            return HttpResponseRedirect(reverse('event_details', kwargs={'event_id': event.id}))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EventForm()

    return render(request, 'events/create.html',  {'form': form})

@login_required(login_url=settings.LOGIN_URL)
def event_details(request, event_id):
    context = {}

    try:
        event = Event.objects.get(id=event_id)
        context['event'] = event
    except Event.DoesNotExist:
        pass
    return render(request, 'events/event_details.html', context)
