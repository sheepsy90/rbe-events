from django.conf.urls import include, url
from django.contrib import admin

import events.views

urlpatterns = [
    # The admin urls and the standard index page url
    url(r'^$', events.views.landing, name='landing'),
    url(r'^admin/', include(admin.site.urls)),

    # The authorization package for RBE Network
    url(r'^', include('rbe_authorize.urls')),
    url(r'^meta/', events.views.meta, name='meta'),
    url(r'^events/', include('events.urls')),
]
