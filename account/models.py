#coding=utf-8

import datetime
from random import random

from signals import email_confirmed,  email_confirmation_sent
from django.conf import settings
from django.db.models.signals import post_save
from django.db import models,  IntegrityError
from django.core.mail import send_mail
from django.core.urlresolvers import reverse,  NoReverseMatch
from django.core.exceptions import *
from django.template.loader import render_to_string
from django.utils.hashcompat import sha_constructor
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

from book.models import *
from main.models import *
from main.db_choices import *

from utils import *

# Create your models here.
class UserProfile(BaseModel):
    user = models.ForeignKey(User, unique=True)
    gender = models.SmallIntegerField(verbose_name=u"性别", default=0, choices=GENDER, null=True, blank=True)
    address = models.CharField(u"地址", max_length=100, null=True, blank=True)
    phone = models.CharField(verbose_name=u"电话号码", max_length=100, null=True, blank=True)
    school = models.ForeignKey(School, verbose_name=u"学校", null=True, blank=True)
    faculty = models.CharField(verbose_name=u"院系", max_length=100,null=True, blank=True)
    major = models.CharField(verbose_name=u"专业", max_length=100,null=True, blank=True)
    score = models.PositiveIntegerField(verbose_name=u"积分", default=0)

    def __unicode__(self):
        return self.user.username

    def fetalerror_action(self, act='', msg=''):
        UserAction.objects.create(user=self.user, level=1, action=act, message=msg)

    def error_action(self, act='', msg=''):
        UserAction.objects.create(user=self.user, level=2, action=act, message=msg)

    def warn_action(self, act='', msg=''):
        UserAction.objects.create(user=self.user, level=3, action=act, message=msg)

    def info_action(self, act='', msg=''):
        UserAction.objects.create(user=self.user, level=4, action=act, message=msg)

    def debug_action(self, act='', msg=''):
        UserAction.objects.create(user=self.user, level=5, action=act, message=msg)

    class Meta: 
        db_table = 'user_profile'
        verbose_name = 'User Profile'

class UserAction(BaseModel):
    user = models.ForeignKey(User)
    level = models.PositiveSmallIntegerField(verbose_name=u'等级', choices=USER_ACTION, default=0)
    created = models.DateTimeField(verbose_name=u'创造日期', auto_now_add=True)
    action = models.CharField(verbose_name=u'动作', max_length=100, blank=True, null=True)
    message = models.TextField(verbose_name=u"信息", blank=True, null=True)

    def __unicode__(self):
        return str(self.id)
    
    class Meta: 
        db_table = 'user_action'
        verbose_name = '用户动作'
        verbose_name_plural = '用户动作'


#class EmailConfirmationManager(models.Manager):
#
#    def confirm_email(self,  confirmation_key):
#        """
#        return confirmation with this confirmation info if verified
#        return false if not
#        """
#        try:
#            confirmation = self.get(confirmation_key=confirmation_key)
#            if not confirmation.key_expired():
#                confirmation.verified = True
#                confirmation.verified_date = datetime.datetime.now()
#                confirmation.save()
#
#                # send email confirmed signal
#                email_confirmed.send(sender=self.model,  confirmation=confirmation)
#
#                return confirmation
#            else:
#                raise Exception("The key is expired")
#        # TODO add log
#        except Exception,  e:
#            return False
#    
#    ###
#    # steps:
#    #    create hex with salt and add it to a specified url
#    #    email the url to user
#    #    create a confirmation info with not verified
#    ###
#    def send_confirmation(self,  user,  email,  confirm_type):
#        """ return the newly created confirmation with this confirmation info """
#        salt = sha_constructor(str(random())).hexdigest()[:5]
#        confirmation_key = sha_constructor(salt + email).hexdigest()
#        current_site = Site.objects.get_current()
#        try:
#            path = reverse("confirm",  kwargs={'confirmation_key':confirmation_key})
#        except:
#            path = reverse("account.views.confirm",  kwargs={'confirmation_key':confirmation_key})
#        protocol = getattr(settings,  "DEFAULT_HTTP_PROTOCOL",  "http")
#        activate_url = u"%s://%s%s" % (protocol,  unicode(current_site.domain),  path)
#        context = {
#            "user": user, 
#            "activate_url": activate_url, 
#            "current_site": current_site, 
#            "confirmation_key": confirmation_key, 
#        }
#        subject = render_to_string("block/email_confirmation_subject.html",  context)
#        subject = "".join(subject.splitlines())
#        message = render_to_string("block/email_confirmation_message.html",  context)
#        send_mail(subject,  message,  settings.DEFAULT_FROM_EMAIL,  [email])
#        confirmation = self.create(
#            user=user, 
#            email=email, 
#            confirm_type = confirm_type, 
#            sent_date=datetime.datetime.now(), 
#            confirmation_key=confirmation_key
#        )
#
#        # send email sent signal 
#        email_confirmation_sent.send(sender=self.model,  confirmation=confirmation)
#
#        return confirmation
#    
#    def delete_expired_confirmations(self):
#        """ clear valueless confirmation record in db """
#        for confirmation in self.all():
#            if confirmation.key_expired():
#                confirmation.delete()
#
#class EmailConfirmation(models.Model):
#    user = models.ForeignKey(User,  unique=True)
#    email = models.EmailField(verbose_name="Email Address")
#    verified = models.BooleanField(verbose_name="Verified",  default=False)
#    confirm_type = models.PositiveSmallIntegerField(verbose_name="Type",  choices=COMFIRM_TYPE)
#    sent_date = models.DateTimeField(verbose_name="Sent Date")
#    verified_date = models.DateTimeField(verbose_name="Verified Date",  null=True,  blank=True)
#    confirmation_key = models.CharField(verbose_name="Confiramtion Key",  max_length=40)
#    
#    objects = EmailConfirmationManager()
#    
#    def key_expired(self):
#        """ return bool,  determining whether the key is expired. """
#        expiration_date = self.sent_date + datetime.timedelta(days=settings.EMAIL_CONFIRMATION_DAYS)
#        return expiration_date <= datetime.datetime.now()
#    key_expired.boolean = True
#    
#    def __unicode__(self):
#        return u"confirmation for %s" % self.email 
#    
#    class Meta:
#        verbose_name = _("Email Confirmation")

