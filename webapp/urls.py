from django.conf.urls import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(('webapp.views'),
        url(r'^home/$', 'home', name='home'),
        url(r'^callin/$', 'callin', name='callin'),
)
