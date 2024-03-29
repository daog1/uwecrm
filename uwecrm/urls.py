from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.conf.urls.static import static
import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'uwecrm.views.home', name='home'),
    # url(r'^uwecrm/', include('uwecrm.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^webapp/', include('webapp.urls')),
    url(r'^identities/', include('identities.urls')),
    url(r'^inquire/', include('Inquire.urls')),
    url(r'^callrecord/', include('CallRecord.urls')),
    url(r'^CallReport/', include('CallReport.urls')),
)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT )
