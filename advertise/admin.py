#coding=utf-8

from django.contrib import admin
from django.contrib.contenttypes import generic

from models import *

from main.admin import *

class AdvertiseAdmin(BaseModelAdmin):
    model = Advertise
    list_display = ('id', 'object', 'title', 'author', 'time', 'agree', 'disagree')
    list_display_links = ('id', 'title')
    list_editable = ('agree', 'disagree')
    search_fields = ['id', 'title',]

admin.site.register(Advertise,AdvertiseAdmin)



