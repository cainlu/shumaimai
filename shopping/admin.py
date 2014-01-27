#coding=utf-8

from django.contrib import admin
from models import *

class DealAdmin(admin.ModelAdmin):
    fieldsets = (
            (
                u'基本信息', 
                {
                    'classes':('grp-collapse grp-open',),
                    'fields':(
                        'status',
                        ('score', 'score_return'),
                        ('address', 'phone'),
                        'remark',
                        ('user', 'ip'),
                        'submitTime',
                    ),
                }
            ),
            (
                u'物流信息', 
                {
                    'classes':('grp-collapse grp-closed',),
                    'fields':(
                        ('deliverMan', 'deliverTime'), 
                        'finishTime',
                        'resultRemark',
                    ),
                }
            ),
        )
    model = Deal
    list_display = ('id','address','phone', 'score', 'submitTime','status', 'user', 'deliverMan', 'resultRemark')
    list_display_links = ('id',)
    list_editable = ('status', 'deliverMan', 'resultRemark')
    list_filter = ('status', 'user')
    raw_id_fields = ('user',)
    readonly_fields = ('submitTime', )
    search_fields = ['id', 'address', 'phone', 'remark']

class Book_DealAdmin(admin.ModelAdmin):
    model = Book_Deal
    list_display = ('id', 'number', 'deal', 'price_buy', 'price_sell', 'url', 'type')
    list_filter = ('type',)
    raw_id_fields = ('book', 'deal')
    search_fields = ['id', 'url', ]

class Sell_DealAdmin(admin.ModelAdmin):
    fieldsets = (
            (
                u'基本信息', 
                {
                    'classes':('grp-collapse grp-open',),
                    'fields':(
                        'status',
                        ('price_all', 'score'), 
                        ('address', 'phone'),
                        'remark',
                        'submitTime',
                    ),
                }
            ),
            (
                u'物流信息', 
                {
                    'classes':('grp-collapse grp-closed',),
                    'fields':(
                        ('deliverMan', 'deliverTime'), 
                        'finishTime',
                        'resultRemark',
                    ),
                }
            ),
        )
    model = Deal
    list_display = ('id','address','phone', 'price_all', 'score', 'submitTime','status', 'deliverMan', 'resultRemark')
    list_display_links = ('id',)
    list_editable = ('status', 'deliverMan', 'resultRemark')
    list_filter = ('status',)
    readonly_fields = ('submitTime', )
    search_fields = ['id', 'address', 'phone', 'remark']


class Sell_Book_DealAdmin(admin.ModelAdmin):
    model = Sell_Book_Deal
    list_display = ('id','number','deal')
    raw_id_fields = ('book', 'deal')
    search_fields = ['id', 'url', ]

admin.site.register(Deal,DealAdmin)
admin.site.register(Book_Deal,Book_DealAdmin)
admin.site.register(Sell_Deal,Sell_DealAdmin)
admin.site.register(Sell_Book_Deal,Sell_Book_DealAdmin)
