from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('account',
    url(r'^login/$', 'views.login', name='user_login'),
    url(r'^logout/$', 'views.logout', name='user_logout'),
    url(r'^register/$', 'views.register', name='user_register'),
    url(r'^user/profile$', 'views.user_profile', name='user_profile'),
    url(r'^user/password/change$', 'views.user_password_change', name='user_password_change'),
    url(r'^captcha_refresh/$', 'views.captcha_refresh', name='captcha_refresh'),
)
