#coding=utf-8

from django.conf import settings

BOOK_DEFAULT_COVER_URL = settings.STATIC_URL + 'image/default_book_cover.jpg'

# DB choices
DIPLOMA = (
    (0, u'未知'),
    (1, u'一本'),
    (2, u'二本'),
    (3, u'高职'),
    (4, u'提前批'),
)

MAJOR_TYPE = (
    (0, u'未知'),
    (1, u'理工'),
    (2, u'文史'),
)

BOOK_LANGUAGE_CHOICES = (
    ('unknown', u'未知'),
    ('other', u'其他'),
    ('zh', u'中文'),
    ('en', u'英文'),
    ('ja', u'日文'),
    ('fr', u'法文'),
    ('ru', u'俄文'),
)

BOOK_STATUS_CHOICES = (
    (0, u'未知'),
    (1, u'销售中'),
    (2, u'已下架'),
    (3, u'边栏推荐'),
    (4, u'待抓取'),
    (5, u'待审核'),
    (6, u'错误'),
)

TAXONOMY_TYPE = (
    (0, u'未知'),
    (1, u'学科'),
)

context_instance = {}

