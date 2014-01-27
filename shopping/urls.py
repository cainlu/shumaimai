from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('shopping',
    url(r'^order/$', 'views.order', name='order'),
    url(r'^ordershow/$', 'views.ordershow', name='ordershow'),
    url(r'^selling/$', 'views.selling', name='selling'),
    url(r'sellshow/$', 'views.sellshow', name='sellshow'),
    url(r'buybehalfshow/$', 'views.buybehalfshow', name='buybehalfshow'),
    url(r'confirmshow/$', 'views.confirmshow', name='confirmshow'),
    url(r'alertshow/$', 'views.alertshow', name='alertshow'),
    url(r'cancelorder/$', 'views.cancelorder', name='cancelorder'),
)
