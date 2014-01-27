#coding=utf-8

import os
import time
import logging

from sphinxapi import *
from book.models import *
from django.db.models import Q
from django.conf import settings
from django.utils.encoding import smart_unicode

logger = logging.getLogger('default')

###
# mode choices: SPH_MATCH_ANY, SPH_MATCH_BOOLEAN, SPH_MATCH_EXTENDED
###

def search(query=u"", host=settings.DEFAULT_SEARCH_SERVER_HOST, port=settings.DEFAULT_SEARCH_SERVER_PORT, 
        mode=SPH_MATCH_ALL, weights=[100, 1], index='*', filtercol='group_id', filtervals=[], 
        sortby='', groupby='', groupsort='@group desc', limit=0):

    if query is not None and query != "":
        cl = SphinxClient()
        cl.SetServer (host, int(port))
        cl.SetWeights (weights)
        cl.SetMatchMode (mode)
        if filtervals:
            cl.SetFilter (filtercol, filtervals)
        if groupby:
            cl.SetGroupBy (groupby, SPH_GROUPBY_ATTR, groupsort)
        if sortby:
            cl.SetSortMode (SPH_SORT_EXTENDED, sortby)
        if limit:
            cl.SetLimits (0, limit, max(limit,1000))
        res = cl.Query (query, index)
        if not res:
            logger.error('query failed: %s' % cl.GetLastError())
        if cl.GetLastWarning():
            logger.warn('WARNING: %s\n' % cl.GetLastWarning())
        if res.has_key('matches'):
            return res['matches']
    return []

def search_book(*args, **kwargs):
    kwargs['index'] = 'book'
    kwargs['weights'] = [100, 100, 80, 50, 50, 50, 10, 10, 10]
    search_res = search(*args, **kwargs)
    id_list = [ res['id'] for res in search_res ]
    id_list_str = ','.join([ str(id) for id in id_list ])
    books = Book.objects.filter(id__in=id_list).extra(
            select={'manual': "FIELD(id, " + id_list_str + ")"},
            order_by=['manual']
            )
    return books

