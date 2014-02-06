#coding=utf-8

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('admin_ext',
    url(r'^$', 'views.home', name='admin_home'),

    url(r'^login$', 'views.login', name='admin_login'),
    url(r'^logout$', 'views.logout', name='admin_logout'),

    url(r'^search$', 'views.admin_book_search', name='admin_book_search'),

    url(r'^book/$', 'views.book_index', name='admin_book_home'),
    url(r'^book/list/$', 'views.book_list', name='admin_book_list'),
    url(r'^book/isbn-add/$', 'views.book_isbn_add', name='admin_book_isbn_add'),
    url(r'^book/create/$', 'views.book_create', name='admin_book_create'),
    url(r'^book/(?P<id>\d+)/edit/$', 'views.book_edit', name='admin_book_edit'),
    url(r'^book/set/$', 'views.book_set', name='admin_book_set'),
    url(r'^book/(?P<id>\d+)/change/cover/$', 'views.book_change_cover', name='admin_book_change_cover'),

    url(r'^order/$', 'views.order_index', name='admin_order_home'),
    url(r'^order/download/$', 'views.order_download', name='admin_order_download'),
    url(r'^order/buy/list/$', 'views.order_buy_list', name='admin_order_buy_list'),
    url(r'^order/buy/(?P<id>\d+)/edit/$', 'views.order_buy_edit', name='admin_order_buy_edit'),
    url(r'^order/buy/set/$', 'views.order_buy_set', name='admin_order_buy_set'),
    url(r'^order/buy/deal/delete/$', 'views.order_book_deal_delete', name='admin_order_book_deal_delete'),
    url(r'^order/buy/deal/(?P<id>\d+)/set/$', 'views.order_buy_detail_set', name='admin_order_buy_detail_set'),
    url(r'^order/sell/list/$', 'views.order_sell_list', name='admin_order_sell_list'),
    url(r'^order/sell/(?P<id>\d+)/edit/$', 'views.order_sell_edit', name='admin_order_sell_edit'),
    url(r'^order/sell/set/$', 'views.order_sell_set', name='admin_order_sell_set'),
    url(r'^order/pick/$', 'views.order_pick_list', name='admin_order_pick_list'),
    url(r'^order/pick/(?P<time_stamp>\d+)/$', 'views.order_pick_show', name='admin_order_pick_show'),
    url(r'^order/pick/finish/(?P<time_stamp>\d+)/$', 'views.order_pick_finish', name='admin_order_pick_finish'),
    url(r'^logistic/set/$', 'views.logistic_set', name='admin_logistic_set'),
    url(r'^logistic/add/$', 'views.logistic_add', name='admin_logistic_add'),
    url(r'^logistic/delete/$', 'views.logistic_delete', name='admin_logistic_delete'),
)


