from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(('CallReport.views'),
    # Examples:
    url(r'^$', 'index',name='index'),
    url(r'^report/$', 'report'),
    url(r'^getListAjax/$', 'getListAjax'),
    )
