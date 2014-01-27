from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.views.generic.simple import redirect_to

urlpatterns = patterns('',
    url(r'^$', include('main.urls')),
    url(r'footer/', include('main.footer_urls')),
    url(r'book/', include('book.urls')),
    url(r'account/', include('account.urls')),
    url(r'search/', include('search.urls')),
    url(r'shopping/', include('shopping.urls')),
    url(r'advertise/', include('advertise.urls')),
    url(r'admin-ext/', include('admin_ext.urls')),
    url(r'captcha/', include('captcha.urls')),
    url(r'image/', include('image.urls')),

    # Special
    url(r'^activity/$', 'advertise.views.advertiseshow'),



    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


handler404 = 'main.views.base_404'
handler500 = 'main.views.base_500'

# Django Grappelli
urlpatterns += patterns('',
    url(r'grappelli/', include('grappelli.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
