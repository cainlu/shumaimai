from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('search',
    url(r'^$','views.search', name='search'),
)
