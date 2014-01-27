from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('advertise',
    url(r'^advertiseshow/$', 'views.advertiseshow', name='advertiseshow'),
    url(r'^advertiseagree/$', 'views.advertiseagree', name='advertiseagree'),
    url(r'^advertisedisagree/$', 'views.advertisedisagree', name='advertisedisagree'),
    url(r'^commentshow/$', 'views.commentshow', name='commentshow'),
    url(r'^messageboard/$', 'views.messageboard', name='messageboard'),
    url(r'^moreadvertise/$', 'views.moreadvertise', name='moreadvertise'),
    url(r'^morecomment/$', 'views.morecomment', name='morecomment'),
    url(r'^welcome-new/$', 'views.welcome_new', name='welcome_new'),
)
