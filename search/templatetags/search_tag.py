#coding=utf-8

from django_jinja.base import Library
from django.core.urlresolvers import reverse

import jinja2, urllib

register = Library()

@register.global_function
def search(query, page=None):
    par = {'query':query}
    if page is not None:
        par['page'] = page
    return reverse('search') + '?' + urllib.urlencode(par) 
        




