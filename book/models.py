#coding=utf-8

import os
import json

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import *
from django.contrib.contenttypes.generic import *

from main.db_choices import *
from main.models import *
from main.utils import *

from utils import *

# Create your models here.

class Taxonomy(BaseModel):
    name = models.CharField(verbose_name=u"名称", max_length=30)
    type = models.SmallIntegerField(verbose_name=u"分类类型", choices=TAXONOMY_TYPE, default=1)
    weight = models.SmallIntegerField(verbose_name=u"权重", default=1)
    level = models.SmallIntegerField(verbose_name=u"级别", default=1)
    parent = models.ForeignKey('self', blank=True, null=True)

    class Meta:
        db_table = "taxonomy"
        verbose_name = u"分类"
        verbose_name_plural = u"分类"
        ordering = ['-weight']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        level = 1
        instance = self
        while True:
            if instance.parent is None:
                break;
            else:
                instance = instance.parent
                level += 1
        self.level = level
        super(Taxonomy, self).save(*args, **kwargs)

    def get_children_id_list(self):
        children = Taxonomy.objects.filter(parent=self)
        res_id_list = list(children.values_list('id', flat=True))
        for t in children:
            res_id_list += t.get_children_id_list()
        return res_id_list

    def get_children(self, include_self=False):
        res_id_list = self.get_children_id_list()
        if include_self:
            res_id_list.append(self.id)
        res_id_list = list(set(res_id_list))
        return Taxonomy.objects.filter(id__in=res_id_list)


    def get_parent(self):
        res = list()
        t = self
        while t.parent:
            t = t.parent 
            res.append(t)
        return res

class TaxonomyIndex(BaseModel):
    taxonomy = models.ForeignKey(Taxonomy)
    content_type = models.ForeignKey(ContentType, related_name='taxonomy_indexes')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.taxonomy.name

    class Meta:
        db_table = 'taxonomy_index'
        verbose_name = u'分类索引'
        verbose_name_plural = u'分类索引'
        unique_together = ('taxonomy', 'content_type', 'object_id')

class Book(BaseModel): 
    name = models.CharField(verbose_name=u"名称", max_length=100, db_index=True)
    subtitle = models.CharField(verbose_name=u"副标题", max_length=100, blank=True, null=True)
    author = models.CharField(verbose_name=u"作者", max_length=50, db_index=True)
    translator = models.CharField(verbose_name=u"译者", max_length=100, blank=True, db_index=True)
    isbn = models.CharField(verbose_name="ISBN", max_length=25, blank=True, null=True, db_index=True)
    press = models.CharField(verbose_name=u"出版社", max_length=100, db_index=True)
    publication_date = models.DateField(verbose_name=u"出版日期", blank=True, null=True)
    version = models.CharField(verbose_name=u"版本", max_length=50, blank=True, null=True)
    language = models.CharField(verbose_name=u"语言", choices=BOOK_LANGUAGE_CHOICES, max_length=10)
    page_number = models.PositiveIntegerField(verbose_name=u"页数", blank=True, null=True)
    size = models.CharField(verbose_name=u"开本", max_length=10, blank=True, null=True)
    binding = models.CharField(verbose_name=u"装帧", max_length=10, blank=True, null=True)
    description = models.TextField(verbose_name=u"描述", blank=True, help_text=u"包括新旧要求，笔记要求")
    image = models.TextField(verbose_name=u"图片", blank=True, null=True, default=json.dumps(dict()))
    recommend = models.TextField(verbose_name=u"书评", blank=True)
    price_ori = models.FloatField(verbose_name=u"原价", default=0)
    price_new = models.FloatField(verbose_name=u"二手书价", default=0)
    price_old = models.FloatField(verbose_name=u"二手书价", default=0)
    status = models.PositiveIntegerField(verbose_name=u"状态", choices=BOOK_STATUS_CHOICES, default=0)
    taxonomy = GenericRelation(TaxonomyIndex, verbose_name=u"分类", null=True, blank=True)
    created = models.DateTimeField(verbose_name=u'创造日期', auto_now_add=True)
    modified = models.DateTimeField(verbose_name=u'修改日期', auto_now=True)
    organization = GenericRelation("OrganizationIndex", null=True, blank=True)
    

    class Meta:
        db_table = "book"
        verbose_name = u"书本"
        verbose_name_plural = u"书本"
        ordering = ['id']

    def __unicode__(self):
        return self.name

    @property
    def image_dict(self):
        try:
            return json.loads(self.image)
        except:
            return dict()

    @image_dict.setter
    def image_dict(self, image_dict):
        if image_dict is None or not isinstance(image_dict, dict):
            image_dict = dict()
        self.image = json.dumps(image_dict)

    @property
    def taxonomy_list(self):
        try:
            list_taxonomy_id = self.taxonomy.all().values_list('taxonomy__id', flat=True)
            res = Taxonomy.objects.filter(id__in=list_taxonomy_id)
            return res
        except:
            return Taxonomy.objects.none()

    @taxonomy_list.setter
    def taxonomy_list(self, taxonomy_list):
        ori_ts_ids = set(self.taxonomy_list.values_list('id', flat=True))
        ts_ids = set([ t.id for t in taxonomy_list ])
        same_ts_ids = ori_ts_ids & ts_ids
        self.taxonomy.filter(taxonomy__id__in=list(ori_ts_ids - same_ts_ids)).delete()
        for t_id in ts_ids - same_ts_ids:
            try:
                TaxonomyIndex(content_object=self, taxonomy=Taxonomy.objects.get(id=t_id)).save()
            except Exception, e:
                pass

    def save(self, *args, **kwargs):
        if self.price_old is None or self.price_old == 0:
            self.price_old = self.price_ori * settings.PRICE_ORI_NOW_RATE
        self.price_old = my_ceil(self.price_old)
        if self.description is None:
            self.description = ''
        self.description = self.description.strip()
        if not self.image_dict.has_key('cover'):
            tmp = self.image_dict
            tmp['cover'] = ''
            self.image_dict = tmp
        super(Book, self).save(*args, **kwargs)

    def get_taxonomy(self):
        list_taxonomy_id = self.taxonomy.all().values_list('taxonomy__id', flat=True)
        res = Taxonomy.objects.filter(id__in=list_taxonomy_id)
        return res

    def add_taxonomy(self, taxonomy):
        TaxonomyIndex(content_object=self, taxonomy=taxonomy).save()
        return self
    
    def add_taxonomies(self, taxonomies):
        for taxonomy in taxonomies:
            try:
                TaxonomyIndex(content_object=self, taxonomy=taxonomy).save()
            except:
                pass
        return self

    def get_logistic_info(self):
        try:
            from logistic.models import Logistic
            ls = Logistic.objects.filter(book=self)
        except Exception, e:
            self._logger.error(e)
            ls = Logistic.objects.none()
        return ls


class School(BaseModel):
    name = models.CharField(verbose_name=u"名称", max_length=50, unique=True)
    web = models.URLField(verbose_name=u"网址", blank=True, null=True)
    weight = models.SmallIntegerField(verbose_name=u"权重", default=1)
    region = models.CharField(verbose_name=u"地址", choices=REGION_CODE, max_length=50)
    ip_start = models.IPAddressField(verbose_name=u"IP起始地址", null=True, blank=True, )
    ip_end = models.IPAddressField(verbose_name=u"IP结束地址", null=True, blank=True, )

    class Meta:
        db_table = "school"
        verbose_name = u"学校"
        verbose_name_plural = u"学校"
        ordering = ['-weight']

    def __unicode__(self):
        return self.name

class Major(BaseModel):
    name = models.CharField(verbose_name=u"名称", max_length=50)
    type = models.SmallIntegerField(verbose_name=u"类型", default=0, choices=MAJOR_TYPE)
    diploma = models.SmallIntegerField(verbose_name=u"学历", default=0, choices=DIPLOMA)
    weight = models.SmallIntegerField(verbose_name=u"权重", default=1)

    class Meta:
        db_table = "major"
        verbose_name = u"院系"
        verbose_name_plural = u"院系" 
        unique_together = ('name', 'type', 'diploma')
        ordering = ['-weight']

    def __unicode__(self):
        return self.name

class Course(BaseModel):
    name = models.CharField(verbose_name=u"名称", max_length=50, unique=True)
    weight = models.SmallIntegerField(verbose_name=u"权重", default=1)

    class Meta:
        db_table = "course"
        verbose_name = u"课程"
        verbose_name_plural = u"课程" 
        ordering = ['-weight']

    def __unicode__(self):
        return self.name

class OrganizationIndex(BaseModel):
    school = models.ForeignKey('School', verbose_name=u"学校")
    major = models.ForeignKey('Major', verbose_name=u"院系")
    course = models.ForeignKey('Course', verbose_name=u"课程", null=True, blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = "school_course_index"
        verbose_name = u"所属组织索引"
        verbose_name_plural = u"所属组织索引"
        unique_together = ('school', 'major', 'course', 'content_type', 'object_id')

    def __unicode__(self):
        return self.school.name + '_' + self.major.name + '_' + self.course.name


