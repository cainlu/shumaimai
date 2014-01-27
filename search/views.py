#coding=utf-8

import json

from django.http import *
from django.shortcuts import *
from django.conf import settings
from django.db.models import Q
from django.core.paginator import *
from django.core.urlresolvers import *
from django.views.decorators.cache import cache_page

from main.utils import *
from book.models import *
from search.utils import *

@cache_page
def search(request):
    context_instance = {}
    query = str(request_get(request, 'query', '', list_allowed=False)).strip()
    page = request_get(request, 'page', list_allowed=False)
    books = []
    fo = request_get(request, 'format', 'page', list_allowed=False)
    if query != u"":
        logging.getLogger('search').info(query)
        book_list = search_book(query=query, limit=500).filter(status__in=[1, 3])
        if fo == 'json':
            res = list()
            for book in book_list[:10]:
                res.append(
                        {
                            'id':book.id,
                            'name':book.name,
                            'author':book.author,
                            'press':book.press,
                            'isbn':book.isbn
                        }
                    )
            return HttpResponse(json.dumps(res, default=my_json_dumps), mimetype="application/json")
        else:
            paginator = Paginator(book_list, settings.ITEMS_NUM_PER_PAGE)
            try:
                books = paginator.page(page)
            except PageNotAnInteger:
                books = paginator.page(1)
            except EmptyPage:
                books = paginator.page(paginator.num_pages)
            context_instance['books'] = books
            context_instance['related_books'] = Book.objects.filter(status=3).order_by('?')
            return render_to_response('page/search_result.jinja', context_instance, RequestContext(request))
    if fo == 'json':
        return HttpResponse(json.dumps([], default=my_json_dumps), mimetype="application/json")
    else:
        return HttpResponseRedirect(reverse('index'))
