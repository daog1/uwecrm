from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(('Inquire.views'),
    # Examples:
    url(r'^$', 'index'),
    url(r'^new/$', 'new'),
    url(r'^edit/$', 'edit'),
    url(r'^save/$', 'save'),
    url(r'^update/(\d+)/$', 'update', name='update'),
    url(r'^getListAjax/$', 'getListAjax'),
    url(r'^getlatelys/$', 'getlatelys'),
    )
