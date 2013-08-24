from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(('CallRecord.views'),
    # Examples:
    url(r'^$', 'index',name='index'),
    url(r'^getListAjax/$', 'getListAjax'),
    )
