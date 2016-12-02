import events.views

from django.conf.urls import url

urlpatterns = [
    url('index', events.views.index, name='index'),
    url('create_event', events.views.create_event, name='create_event'),
    url('event_details/(?P<event_id>\d*)$', events.views.event_details, name='event_details'),
]
