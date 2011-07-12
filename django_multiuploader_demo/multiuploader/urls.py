from django.conf.urls.defaults import *

from multiuploader.views import multiuploader_delete

urlpatterns = patterns('',
    (r'^delete/(\d+)/$', multiuploader_delete),
    url(r'^$', 'django_multiuploader_demo.multiuploader.views.image_view', name='main'),
    url(r'^multi/$', 'django_multiuploader_demo.multiuploader.views.multiuploader', name='multi'),
    
)
