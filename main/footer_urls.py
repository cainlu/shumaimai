from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('main',
    url(r'about-us/$', 'views.footer_about_us', name='footer_about_us'),
    url(r'contact-us/$', 'views.footer_contact_us', name='footer_contact_us'),
    url(r'job/$', 'views.footer_job', name='footer_job'),
    url(r'buy/$', 'views.footer_buy', name='footer_buy'),
    url(r'sell/$', 'views.footer_sell', name='footer_sell'),
    url(r'subscribe/$', 'views.footer_subscribe', name='footer_subscribe'),
    url(r'quality/$', 'views.footer_quality', name='footer_quality'),
    url(r'return/$', 'views.footer_return', name='footer_return'),
)

