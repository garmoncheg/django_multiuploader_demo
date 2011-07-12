from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from models import Image
from django.core.files.uploadedfile import UploadedFile
from django.template import RequestContext

#importing json parser to generate plugin friendly json response
from django.utils import simplejson

#for generating thumbnails
#sorl-thumbnails must be installed and properly configured
from sorl.thumbnail import get_thumbnail


from django.views.decorators.csrf import csrf_exempt

import logging
log = logging

@csrf_exempt
def multiuploader_delete(request, pk):
    """
    View for deleting photos with multiuploader AJAX plugin.
    made from api on:
    https://github.com/blueimp/jQuery-File-Upload
    """
    if request.method == 'POST':
        log.info('Called delete image. Photo id='+str(pk))
        image = get_object_or_404(Image, pk=pk)
        image.delete()
        log.info('DONE. Deleted photo id='+str(pk))
        return HttpResponse(str(pk))
    else:
        log.info('Recieved not POST request todelete image view')
        return HttpResponseBadRequest('Only POST accepted')

@csrf_exempt
def multiuploader(request):
    if request.method == 'POST':
        log.info('received POST to main multiuploader view')
        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')

        #getting file data for farther manipulations
        file = request.FILES[u'files[]']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size
        log.info ('Got file: "'+str(filename)+'"')

        #writing file manually into model
        #because we don't need form of any type.
        image = Image()
        image.title=str(filename)
        image.image=file
        image.save()
        log.info('File saving done')

        #getting url for photo deletion
        file_delete_url = '/delete/'
        
        #getting file url here
        file_url = '/'

        #getting thumbnail url using sorl-thumbnail
        im = get_thumbnail(image, "80x80", quality=50)
        thumb_url = im.url

        #generating json response array
        result = []
        result.append({"name":filename, 
                       "size":file_size, 
                       "url":file_url, 
                       "thumbnail_url":thumb_url,
                       "delete_url":file_delete_url+str(image.pk)+'/', 
                       "delete_type":"POST",})
        response_data = simplejson.dumps(result)
        return HttpResponse(response_data, mimetype='application/json')
    else: #GET
        return render_to_response('multiuploader_main.html', 
                                  {'static_url':settings.MEDIA_URL,
                                   'open_tv':u'{{',
                                   'close_tv':u'}}'}, 
                                  )

def image_view(request):
    items = Image.objects.all()
    return render_to_response('images.html', {'items':items})


