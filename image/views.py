#coding=utf-8

import os
from cStringIO import StringIO

from django.shortcuts import *
from django.http import *
from django.conf import settings
from django.views.decorators.cache import cache_page

from main.utils import *

from utils import *

@cache_page
def image_get(request):
    par_mode = request_get(request, 'mode', list_allowed=False)
    par_width = request_get(request, 'width', list_allowed=False)
    par_height = request_get(request, 'height', list_allowed=False)
    path = os.path.join(settings.STATIC_ROOT, request.path[1:])
    res = image_factory(path=path, mode=par_mode, width=par_width, height=par_height)
    tmp = StringIO()
    try:
        im_type = str(settings.IMAGE_TYPE[path[-3:]])
        res.save(tmp, im_type)
    except:
        im_type = 'png'
        res.save(tmp, im_type)
    return HttpResponse(tmp.getvalue(), mimetype="image/" + im_type)

