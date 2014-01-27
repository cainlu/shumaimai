#coding=utf-8

from django.db import models
from book.models import *
from django.contrib.auth.models import User
import datetime

DEAL_STATUS_CHOICES = (
            (0,u'未知'),
            (1,u'已完成'),
            (2,u'丢弃'),
            (3,u'处理中'),
            (4,u'递送中'),
            (5,u'取消'),
            (6,u'代购送货中'),
        )

PAY_WAY_CHOICES = (
            (0,u'未知'),
            (1,u'统一'),
            (2,u'分开'),
        )

BUY_STATUS_CHOICES= (
            (0,u'未知'),
            (1,u'正常购买'),
            (2,u'url代购'),
            (3,u'书名代购'),
        )

SELL_DEAL_STATUS_CHOICES = (
            (0,u'未知'),
            (1,u'已完成'),
            (2,u'丢弃'),
            (3,u'处理中'),
            (4,u'递送中'),
            (5,u'取消'),
        )

PAY_STATUS_CHOICES = (
            (0,u'未知'),
            (1,u'现金'),
            (2,u'餐饮折扣券(9折)'),
            (3,u'书麦麦购书抵用券'),
        )

class Deal(models.Model):
    id = models.CharField(primary_key=True,verbose_name=u"订单id",max_length=100)
    status = models.PositiveIntegerField(verbose_name=u"状态",choices=DEAL_STATUS_CHOICES,default=0)
    address = models.CharField(verbose_name=u"地址",max_length=100)
    phone = models.CharField(verbose_name=u"电话号码",max_length=100)
    remark = models.TextField(verbose_name=u"备注",blank=True,null=True)
    user = models.ForeignKey(User, verbose_name=u"用户id",blank=True,null=True)
    score = models.PositiveIntegerField(verbose_name=u"消耗积分",default=0)
    score_return = models.PositiveIntegerField(verbose_name=u"返还积分",default=0)
    ip = models.IPAddressField(verbose_name=u"IP网址",blank=True,null=True)
    submitTime = models.DateTimeField(verbose_name=u"订单提交时间",auto_now_add=True)
    deliverMan = models.PositiveIntegerField(verbose_name=u"递送人员",blank=True,default=0,null=True)
    deliverTime = models.DateTimeField(verbose_name=u"递送开始时间",blank=True,null=True)
    finishTime = models.DateTimeField(verbose_name=u"交易完成时间",blank=True,null=True)
    resultRemark = models.TextField(verbose_name=u"结果备注",blank=True,null=True)
    
    def __unicode__(self):
        return u"%s" % self.id

    def save(self, *args, **kwargs):
        if self.status == 4 and not self.deliverTime:
            self.deliverTime = datetime.datetime.now()
        if (self.status == 1 or self.status == 2 or self.status == 5) and not self.finishTime:
            self.finishTime = datetime.datetime.now()
        super(Deal, self).save(*args, **kwargs)

    def get_book_deals(self):
        return Book_Deal.objects.filter(deal=self)

    class Meta:
        db_table = "deal"
        verbose_name = u"买书订单"
        verbose_name_plural = u"买书订单"

class Book_Deal(models.Model):
    book = models.ForeignKey(Book, verbose_name=u"书籍id",blank=True,null=True)
    url = models.URLField(verbose_name=u"代购网址",blank=True,null=True)
    number = models.PositiveIntegerField(verbose_name=u"订购数量")
    price_buy = models.FloatField(verbose_name=u"买入价格", default=0)
    price_sell = models.FloatField(verbose_name=u"成交价格", default=0)
    deal = models.ForeignKey(Deal, verbose_name=u"订单id")
    type = models.PositiveIntegerField(verbose_name=u"购买类型",choices=BUY_STATUS_CHOICES,default=0)
    
    def __unicode__(self):
        return u"%s" % self.deal

    class Meta:
        db_table = "book_deal"
        verbose_name = u"买书订单明细"
        verbose_name_plural = u"买书订单明细"

class Sell_Deal(models.Model):
    id = models.CharField(primary_key=True,verbose_name=u"订单id",max_length=100)
    status = models.PositiveIntegerField(verbose_name=u"状态",choices=SELL_DEAL_STATUS_CHOICES,default=0)
    address = models.CharField(verbose_name=u"地址",max_length=100)
    phone = models.CharField(verbose_name=u"电话号码",max_length=100)
    score = models.PositiveIntegerField(verbose_name=u"积分",default=0)
    remark = models.TextField(verbose_name=u"备注",blank=True,null=True)
    price_all = models.FloatField(verbose_name=u"合计价格", default=0)
    submitTime = models.DateTimeField(verbose_name=u"订单提交时间",auto_now_add=True)
    deliverMan = models.PositiveIntegerField(verbose_name=u"递送人员",blank=True,default=0,null=True)
    deliverTime = models.DateTimeField(verbose_name=u"递送开始时间",blank=True,null=True)
    finishTime = models.DateTimeField(verbose_name=u"交易完成时间",blank=True,null=True)
    resultRemark = models.TextField(verbose_name=u"结果备注",blank=True,null=True)
    
    def __unicode__(self):
        return u"%s" % self.id

    def save(self, *args, **kwargs):
        if self.status == 4 and not self.deliverTime:
            self.deliverTime = datetime.datetime.now()
        if (self.status == 1 or self.status == 2 or self.status == 5) and not self.finishTime:
            self.finishTime = datetime.datetime.now()
        super(Sell_Deal, self).save(*args, **kwargs)

    def get_book_deals(self):
        return Book_Deal.objects.filter(deal=self)

    class Meta:
        db_table = "sell_deal"
        verbose_name = u"卖书订单"
        verbose_name_plural = u"卖书订单"

class Sell_Book_Deal(models.Model):
    book = models.ForeignKey(Book, verbose_name=u"书籍id",blank=True,null=True)
    number = models.PositiveIntegerField(verbose_name=u"出手数量")
    deal = models.ForeignKey(Sell_Deal, verbose_name=u"订单id")
    
    def __unicode__(self):
        return u"%s" % self.dealid

    class Meta:
        db_table = "sell_book_deal"
        verbose_name = u"卖书订单明细"
        verbose_name_plural = u"卖书订单明细"

