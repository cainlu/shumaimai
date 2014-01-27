#coding=utf-8

from django.shortcuts import *
from django.core.paginator import *
from django.http import *
from django.views.decorators.cache import *

from main.utils import *

from models import *
from utils import *

@cache_page
def page_book(request, book_id):
    # TODO 需要个算法
    related_books = Book.objects.filter(status=3).order_by('?')
    return render_to_response(
            'page/book.jinja', 
            {
                'book':Book.objects.get(id=book_id),
                'related_books':related_books,
            }, 
            RequestContext(request)
        )

@cache_page
def page_taxonomy(request, taxonomy_id):
    page = request.GET.get('page')
    context_instance = {
            'related_books':Book.objects.filter(status=3).order_by('?'),
        }
    t = Taxonomy.objects.get(id=taxonomy_id)
    book_list = Book.objects.filter(taxonomy__taxonomy__id__in=t.get_children_id_list() + [t.id], status=1)
    paginator = Paginator(book_list, settings.ITEMS_NUM_PER_PAGE)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    context_instance['books'] = books
    return render_to_response('page/taxonomy.jinja', context_instance, RequestContext(request))

