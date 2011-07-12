from django.conf.urls.defaults import *
import os.path
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^django_multiuploader_demo/', include('django_multiuploader_demo.foo.urls')),
    
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'', include('multiuploader.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 
            os.path.join(settings.PROJECT_ROOT, 'media/').replace('\\','/'),
            'show_indexes': True}),
    )