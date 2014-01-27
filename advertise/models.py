#coding=utf-8

from django.db import models

IP_ACTION_CHOICES = (
            (0,u'无'),
            (1,u'agree'),
            (2,u'disagree'),
        )

TEXT_TYPE_CHOICES = (
            (0,u'无'),
            (1,u'散文'),
            (2,u'插画'),
        )

ACTIVITY_CHOICES = (
            (0,u'无'),
            (1,u'学雷锋'),
            (2,u'读书节'),
        )

class Advertise(models.Model):
    object = models.IntegerField(verbose_name=u"目标对象",max_length=100)
    title = models.CharField(verbose_name=u"标题",max_length=100,blank=True,null=True)
    author = models.CharField(verbose_name=u"作者",max_length=100,blank=True,null=True)
    context = models.TextField(verbose_name=u"内容",blank=True,null=True)
    time = models.DateTimeField(verbose_name=u"提交时间",blank=True,null=True)
    agree = models.PositiveIntegerField(verbose_name=u"赞一个",default=0)
    disagree = models.PositiveIntegerField(verbose_name=u"打酱油",default=0)
    type = models.PositiveIntegerField(verbose_name=u"文章类型",choices=TEXT_TYPE_CHOICES,default=0)
    activity = models.PositiveIntegerField(verbose_name=u"活动",choices=ACTIVITY_CHOICES,default=0)

    class Meta:
        db_table = "advertise"
        verbose_name = u"文章"
        verbose_name_plural = u"文章"
    
    def __unicode__(self):
        return u"%s" % self.title

class Ad_Text(models.Model):
    title = models.CharField(verbose_name=u"标题",max_length=100,blank=True,null=True)
    author = models.CharField(verbose_name=u"作者",max_length=100,blank=True,null=True)
    context = models.TextField(verbose_name=u"内容",blank=True,null=True)
    time = models.DateTimeField(verbose_name=u"提交时间",blank=True,null=True)
    agree = models.PositiveIntegerField(verbose_name=u"赞一个",default=0)
    disagree = models.PositiveIntegerField(verbose_name=u"打酱油",default=0)
    type = models.PositiveIntegerField(verbose_name=u"文章类型",choices=TEXT_TYPE_CHOICES,default=0)
    activity = models.PositiveIntegerField(verbose_name=u"活动",choices=ACTIVITY_CHOICES,default=0)

    class Meta:
        db_table = "ad_text"
        verbose_name = u"文章"
        verbose_name_plural = u"文章"
    
    def __unicode__(self):
        return u"%s" % self.title

class Ad_Comment(models.Model):
    object = models.IntegerField(verbose_name=u"目标对象",max_length=100)
    author = models.CharField(verbose_name=u"作者",max_length=100,blank=True,null=True)
    context = models.TextField(verbose_name=u"内容",blank=True,null=True)
    time = models.DateTimeField(verbose_name=u"提交时间",blank=True,null=True)
    agree = models.PositiveIntegerField(verbose_name=u"赞一个",default=0)
    disagree = models.PositiveIntegerField(verbose_name=u"打酱油",default=0)
    activity = models.PositiveIntegerField(verbose_name=u"活动",choices=ACTIVITY_CHOICES,default=0)

    class Meta:
        db_table = "ad_comment"
        verbose_name = u"评论"
        verbose_name_plural = u"评论"
    
    def __unicode__(self):
        return u"%s" % self.context

class Ip_Record(models.Model):
    ip = models.IPAddressField(verbose_name=u"IP地址")
    action = models.PositiveIntegerField(verbose_name=u"动作",choices=IP_ACTION_CHOICES,default=0)
    object = models.IntegerField(verbose_name=u"目标对象",max_length=100)
    activity = models.PositiveIntegerField(verbose_name=u"活动",choices=ACTIVITY_CHOICES,default=0)
    
    class Meta:
        db_table = "ip_record"
        verbose_name = u"IP记录"
        verbose_name_plural = u"IP记录"
    
    def __unicode__(self):
        return u"%s" % self.ip
