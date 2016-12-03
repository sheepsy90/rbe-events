import datetime
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from events.forms import EventForm
from events.models import Event, EventParticipant, PARTICIPATION_STATES


def landing(request):
    if hasattr(request, 'user') and request.user.is_authenticated:
        return HttpResponseRedirect(settings.AFTER_LOGIN_URL)
    return render(request, 'events/landing.html')


@login_required(login_url=settings.LOGIN_URL)
def index(request):

    search_language = request.GET.get('search_language', 'all')
    search_distance = request.GET.get('search_distance', '0')
    search_text = request.GET.get('search_text', '')

    try:
        search_distance = int(search_distance)
        assert search_distance in [0, 20, 50, 100, 500]
    except:
        search_distance = 0

    try:
        assert search_language in ['all', 'mine']
    except:
        search_language = 'all'

    todays_date = timezone.datetime.today().date()

    event_qs = Event.objects.filter(begin_time__gte=todays_date)

    if search_text:
        # Allow only stuff that matches the title
        event_qs = event_qs.filter(Q(title__icontains=search_text)|Q(description__icontains=search_text))

    if search_language == 'mine':
        # Filter based on user languages
        # TODO implement
        pass

    if search_distance != 0:
        # Filter based on user's distance to event
        # TODO implement
        pass

    event_qs = event_qs.order_by('begin_time')

    context = {
        'events': event_qs,
        'search_language': search_language,
        'search_distance': search_distance,
        'search_text': search_text
    }

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
        context['participants'] = EventParticipant.objects.filter(event=event)

        ep_qs = EventParticipant.objects.filter(event=event, user=request.user)
        if ep_qs.exists():
            context['participation_status'] = ep_qs.first()

    except Event.DoesNotExist:
        pass
    return render(request, 'events/event_details.html', context)


@login_required(login_url=settings.LOGIN_URL)
def edit_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist as e:
        return render(request, 'events/edit.html', {'error': "The event you try to edit doesn't exists"})

    if event.creator != request.user:
        return render(request, 'events/edit.html', {'error': "Sorry, you cannot edit this event"})

    if request.method == 'POST':
        # This is the save changed events call
        form = EventForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            language = form.cleaned_data['language']
            medium = form.cleaned_data['medium']
            begin_time = form.start_datetime
            end_time = form.end_datetime

            event.title = title
            event.description = description
            event.language = language
            event.medium = medium
            event.begin_time = begin_time
            event.end_time = end_time
            event.save()

            # TODO - add email send out when event timings change
            return HttpResponseRedirect(reverse('event_details', kwargs={'event_id': event.id}))

    else:
        form = EventForm(initial={
            'title': event.title,
            'description': event.description,
            'language': event.language,
            'medium': event.medium,
            'start_date': event.begin_time.strftime("%Y-%m-%d"),
            'start_time': event.begin_time.strftime("%H:%M"),
            'end_time': event.end_time.strftime("%H:%M"),
            'end_date': event.end_time.strftime("%Y-%m-%d")
        })

    return render(request, 'events/edit.html', {'form': form, 'event': event})


@login_required(login_url=settings.LOGIN_URL)
def event_pstatus(request):
    event_id = request.POST.get('event_id')
    new_state = request.POST.get('new_state')

    try:
        event = Event.objects.get(id=event_id)

        if new_state not in dict(PARTICIPATION_STATES).keys():
            return JsonResponse({'success': False, 'reason': "Unknown new state!"})

        ep, created = EventParticipant.objects.get_or_create(event=event, user=request.user)
        ep.state = new_state
        ep.save()
        return JsonResponse({'success': True})

    except Event.DoesNotExist:
        return JsonResponse({'success': False, 'reason': "No such event!"})
