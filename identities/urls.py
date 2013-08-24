from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(('identities.views'),
    # Examples:
    url(r'^$', 'index', name='index'),
    url(r'^new/$', 'new', name='new'),
    url(r'^save/$', 'save', name='save'),
    url(r'^edit/$', 'edit', name='edit'),
    url(r'^update/(\d+)/$', 'update', name='update'),
    url(r'^getListAjax/$', 'getListAjax', name='getListAjax'),


    #url(r'^callin/$', 'callin', name='callin'),
)
