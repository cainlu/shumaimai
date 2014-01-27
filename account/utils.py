#coding=utf-8

context_instance = {}

try:
    from main.utils import context_instance as context_instance_main
    context_instance = dict(context_instance_main, context_instance)
except:
    pass

# DB Choices

USER_ACTION = (
    (0, u'未知'),
    (1, u'致命错误'),
    (2, u'错误'),
    (3, u'警告'),
    (4, u'信息'),
    (5, u'调试'),
)


GENDER = (
    (0, u'未知'),
    (1, u'男'),
    (2, u'女'),
)

