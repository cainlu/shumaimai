#coding=utf-8

import logging

from django.db import models
from django.forms.models import model_to_dict


class BaseQuerySet(models.query.QuerySet):
    pass

class BaseModelManager(models.Manager):
    
    _logger = logging.getLogger('default')


class BaseModel(models.Model):

    _logger = logging.getLogger('default')

    objects = BaseModelManager()

    def as_dict(self):
        return model_to_dict(self)

    class Meta:
        abstract = True


