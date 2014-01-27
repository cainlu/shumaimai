from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('book.views',
    url(r'^(?P<book_id>\d+)/$', 'page_book', name='page_book'),
    url(r'^taxonomy/(?P<taxonomy_id>\d+)/$', 'page_taxonomy', name='page_taxonomy'),
)
