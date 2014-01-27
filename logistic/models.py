#coding=utf-8

import os

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import *
from django.contrib.contenttypes.generic import *

from main.db_choices import *
from main.models import *
from book.models import Book

# Create your models here.

class Logistic(BaseModel):
    book = models.ForeignKey(Book, verbose_name=u"书本", blank=True, null=True)
    number = models.PositiveIntegerField(verbose_name=u"库存", default=0, db_index=True)
    position = models.CharField(verbose_name=u"库位", max_length=50, db_index=True)
    remark = models.TextField(verbose_name=u"备注", blank=True, null=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table = "logistic"
        unique_together = ('book', 'position')
        verbose_name = u"仓储"
        verbose_name_plural = u"仓储"


