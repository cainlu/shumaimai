#coding=utf-8

from django.core.signals import * 
from django.db.models.signals import *
from django.dispatch import receiver
from django.core.exceptions import *
from django.contrib.auth import models as auth_models 

import models as account_models
from models import *

@receiver(post_syncdb, sender=auth_models)
def auth_init(sender, **kwargs):
    try:
        auth_models.User.objects.get(id=1)
    except ObjectDoesNotExist:
        ori_user = auth_models.User.objects.create_superuser(
                username = "cula",
                password = "test",
                email = "culahuang@gmail.com",
            )
        UserProfile.objects.get_or_create(user=ori_user)
    except MultipleObjectsReturned:
        raise Exception("To many origin user with id = 1!")


