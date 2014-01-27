#coding=utf-8

from django.contrib import admin
from django.contrib.contenttypes import generic

from models import *

from main.admin import *

class SchoolAdmin(BaseModelAdmin):
    fieldsets = (
            (
                u'基本信息', 
                {
                    'classes':('grp-collapse grp-open',),
                    'fields':(
                        'name',
                        'weight',
                        'region',
                    ),
                }
            ),
            (
                u'在线信息', 
                {
                    'classes':('grp-collapse grp-closed',),
                    'fields':(
                        'web', 
                        ('ip_start', 'ip_end'),
                    ),
                }
            ),
        )
    model = School
    list_display = ('id', 'name', 'weight', 'region', 'ip_start', 'ip_end')
    list_display_links = ('id', 'name')
    list_editable = ('weight', 'region')
    list_filter = ('region',)
    search_fields = ['web', 'ip_start', 'ip_end']

class MajorAdmin(BaseModelAdmin):
    fieldsets = (
            (
                u'基本信息', 
                {
                    'classes':('grp-collapse grp-open',),
                    'fields':(
                        'name',
                        'type', 'diploma', 'weight',
                    ),
                }
            ),
        )
    model = Major
    list_display = ('id', 'name', 'type', 'diploma', 'weight')
    list_display_links = ('id', 'name')
    list_editable = ('diploma', 'weight')
    search_fields = ['name',]


class CourseAdmin(BaseModelAdmin):
    fieldsets = (
            (
                u'基本信息', 
                {
                    'classes':('grp-collapse grp-open',),
                    'fields':(
                        'name',
                        'weight',
                    ),
                }
            ),
        )
    model = Course
    list_display = ('id', 'name', 'weight')
    list_display_links = ('id', 'name')
    list_editable = ('weight',)
    search_fields = ['name',]


class OrganizationIndexInline(generic.GenericTabularInline):
    extra = 1
    raw_id_fields = ('school', 'major', 'course')
    model = OrganizationIndex
    classes = ('grp-collapse grp-closed',)
    inline_classes = ('grp-collapse grp-closed',)

class TaxonomyIndexInline(generic.GenericTabularInline):
    extra = 1
    raw_id_fields = ('taxonomy',)
    model = TaxonomyIndex
    classes = ('grp-collapse grp-closed',)
    inline_classes = ('grp-collapse grp-closed',)

class TaxonomyAdmin(BaseModelAdmin):
    fieldsets = (
            (
                u'基本信息', 
                {
                    'classes':('grp-collapse grp-open',),
                    'fields':(
                        'name', 
                        'weight',
                        'level',
                        'parent',
                    ),
                }
            ),
        )
    model = Taxonomy
    list_display = ('id', 'name', 'weight', 'level', 'parent')
    list_display_links = ('id', 'name')
    list_editable = ('weight', 'level', 'parent')
    list_filter = ('level','parent')
    search_fields = ['name', ]

class BookAdmin(BaseModelAdmin):

    fieldsets = (
            (
                u'基本信息', 
                {
                    'classes':('grp-collapse grp-open',),
                    'fields':(
                        'id',
                        'isbn',
                        ('name', 'subtitle'), 
                        ('author', 'translator'),
                        ('press', 'publication_date'),
                        ('price_ori', 'price_old'),
                        'status',
                        ('created', 'modified'),
                    ),
                }
            ),
            (
                u'详细信息', 
                {
                    'classes':('grp-collapse grp-closed',),
                    'fields':(
                        'page_number',
                        'size',
                        'binding',
                        'language',
                        'version',
                        'description',
                        'recommend',
                        'image',
                    ),
                }
            ),
        )
    inlines = [OrganizationIndexInline, TaxonomyIndexInline]
    model = Taxonomy
    list_display = ('id',  'name', 'isbn', 'author', 'press', 'price_old', 'status', 'created', 'modified')
    list_display_links = ('id', 'name')
    list_editable = ('status', 'price_old')
    list_filter = ('status', 'taxonomy', 'organization')
    readonly_fields = ('id', 'created', 'modified')
    search_fields = ['id', 'name', 'author', 'translator', 'isbn', 'press', 'description']

admin.site.register(Book,BookAdmin)
admin.site.register(School,SchoolAdmin)
admin.site.register(Major,MajorAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Taxonomy,TaxonomyAdmin)



