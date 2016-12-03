import events.views

from django.conf.urls import url

urlpatterns = [
    url('index', events.views.index, name='index'),
    url('create_event', events.views.create_event, name='create_event'),
    url('event_pstatus', events.views.event_pstatus, name='event_pstatus'),
    url('edit_event/(?P<event_id>\d*)$', events.views.edit_event, name='edit_event'),
    url('event_details/(?P<event_id>\d*)$', events.views.event_details, name='event_details'),
]
