from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('main',
    url(r'^$', 'views.index', name='index'),
)

