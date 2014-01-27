#coding=utf-8

from django.http import *
from django.core.urlresolvers import reverse

class admin_auth_required(object):

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):  
        try:
            if not args[0].user.is_anonymous():
                return self.func(*args, **kwargs)  
            else:
                raise
        except:
            return HttpResponseRedirect(reverse('admin_login'))

class admin_auth_is_staff_required(object):

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):  
        try:
            if args[0].user.is_staff:
                return self.func(*args, **kwargs)  
            else:
                raise
        except Exception, e:
            print e
            return HttpResponseRedirect(reverse('admin_login'))

class admin_auth_is_superuser_required(object):

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):  
        try:
            if args[0].user.is_superuser:
                return self.func(*args, **kwargs)  
            else:
                raise
        except Exception, e:
            print e
            return HttpResponseRedirect(reverse('admin_login'))



