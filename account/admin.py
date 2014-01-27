#coding=utf-8

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group 
from django.db.models.signals import *
from django.dispatch import *
from django.core.exceptions import *
from django.contrib.sites.models import Site
from django.conf import settings

from models import *
from signals import *

from main.admin import *

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]

class UserActionAdmin(BaseModelAdmin):
    list_display = ('id', 'level', 'action', 'user', 'created', 'message')
    list_filter = ('level', 'user')
    raw_id_fields = ('user',)
    readonly_fields = ('created', )
    search_fields = ['id', 'action', 'message']

#class EmailConfirmationAdmin(admin.ModelAdmin):
#    model = EmailConfirmation
#    list_display = ('id', 'user', 'email', 'verified', 'sent_date', 'verified_date', 'confirmation_key')

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(UserAction, UserActionAdmin)
#admin.site.register(EmailConfirmation, EmailConfirmationAdmin)

# initial new user according to requirement
@receiver(post_save, sender=User)
def create_user_extra(sender, instance, created, **kwargs):
    """
    initial new user:
    set is_active = False
    set groups = null
    create user profile if needed
    """
    if created:
        #instance.is_active = False
        instance.save()
        UserProfile.objects.get_or_create(user=instance)


