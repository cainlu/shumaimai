#coding=utf-8

from django.contrib import admin
from django.contrib.contenttypes import generic

from models import *

from main.admin import *

class LogisticAdmin(BaseModelAdmin):
    model = Logistic
    list_display = ('id',  'book', 'number', 'position', )
    list_editable = ('number', 'position', )
    list_filter = ('book',)
    raw_id_fields = ('book',)
    search_fields = ['position', ]

admin.site.register(Logistic, LogisticAdmin)
