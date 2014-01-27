#coding=utf-8

from django.conf.urls.defaults import patterns, include, url

from views import *

urlpatterns = patterns('image.views',
    url(r'$', 'image_get', name="image_get"),
)

