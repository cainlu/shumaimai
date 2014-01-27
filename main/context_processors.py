#coding=utf-8

from book.models import *
from account.forms import *
from shopping.models import *

from utils import request_get

def basic(request):
    return {
        'query':request_get(request, 'query', '', list_allowed=False),
        # TODO 这里需要个算法
        'hot_books':Book.objects.all()[:5],

        'taxonomys':Taxonomy.objects.filter(level=1,weight__gt=1)[:3],

    }
