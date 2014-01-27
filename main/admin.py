#coding=utf-8

import logging

from django.contrib import admin

class BaseModelAdmin(admin.ModelAdmin):

    _logger = logging.getLogger('default')

    list_max_show_all = 1000
    list_per_page = 50
    save_as = True
    save_on_top = True

