import events.views

from django.conf.urls import url

urlpatterns = [
    url('index', events.views.index, name='index'),
]
