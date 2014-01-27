#coding=utf-8

from django import forms

from captcha.fields import CaptchaField

from main.utils import *
from main.forms import *
from book.models import *

from models import *
from utils import *

class UserForm(BasicForm):
    email = forms.EmailField(label=u'邮件地址',required=False)
    address = forms.CharField(label=u'联系地址', required=False)
    phone = forms.IntegerField(label=u'联系电话', required=False)
    last_name = forms.CharField(label=u'姓', required=False)
    first_name = forms.CharField(label=u'名', required=False)
    gender = forms.ChoiceField(label=u'性别', choices=GENDER[1:], required=False)
    school = forms.ModelChoiceField(label=u'学校', queryset=School.objects.all(), empty_label=None, required=False)
    faculty = forms.CharField(label=u'院系', required=False)
    major = forms.CharField(label=u'专业', required=False)
    captcha = CaptchaField(label=u'验证码', required=True, error_messages={'invalid':'验证码错误'})

    required_css_class = 'required'

class RegisterForm(BasicForm):
    username = forms.CharField(label=u'用户名', max_length=30, required=True)
    password = forms.CharField(label=u'登录密码', max_length=30, required=True, widget=forms.PasswordInput)
    password_again = forms.CharField(label=u'重复密码', max_length=30, required=True, widget=forms.PasswordInput)
    email = forms.EmailField(label=u'邮件地址',required=False)
    address = forms.CharField(label=u'联系地址', required=False)
    phone = forms.IntegerField(label=u'联系电话', required=False)
    school = forms.ModelChoiceField(label=u'学校', queryset=School.objects.all(), empty_label=None, required=False)
    captcha = CaptchaField(label=u'验证码', required=True, error_messages={'invalid':'验证码错误'})

    required_css_class = 'required'

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        if self.errors:
            return cleaned_data
        if User.objects.filter(username=dict_get(cleaned_data, 'username')).exists():
            self._errors["username"] = self.error_class([u"该用户名已存在"])
            return cleaned_data
        elif dict_get(cleaned_data, 'password')!=dict_get(cleaned_data, 'password_again'):
            self._errors["password_again"] = self.error_class([u"两次输入的密码不一致"])
            return cleaned_data
        return cleaned_data

class LoginForm(BasicForm):
    username = forms.CharField(label=u'用户名', max_length=30, required=True)
    password = forms.CharField(label=u'登录密码', max_length=30, required=True, widget=forms.PasswordInput)
    captcha = CaptchaField(label=u'验证码', required=True, error_messages={'invalid':'验证码错误'})

    required_css_class = 'required'

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        if self.errors:
            return cleaned_data
        username = dict_get(cleaned_data, 'username')
        password = dict_get(cleaned_data, 'password')
        try:
            user = User.objects.get(username=username, is_active=True)
        except Exception, e:
            self._errors["username"] = self.error_class([u"该用户名不存在"])
            return cleaned_data
        else:
            if user.check_password(password):
                return cleaned_data
            else:
                self._errors["password"] = self.error_class([u"密码错误"])
                return cleaned_data


class PasswordChangeForm(BasicForm):
    password_old = forms.CharField(label=u'旧密码', max_length=30, required=True, widget=forms.PasswordInput)
    password_new = forms.CharField(label=u'新密码', max_length=30, required=True, widget=forms.PasswordInput)
    password_new_again = forms.CharField(label=u'密码确认', max_length=30, required=True, widget=forms.PasswordInput)
    captcha = CaptchaField(label=u'验证码', required=True, error_messages={'invalid':'验证码错误'})

    def clean(self):
        cleaned_data = super(PasswordChangeForm, self).clean()
        if self.errors:
            return cleaned_data
        password_old = dict_get(cleaned_data, 'password_old')
        password_new = dict_get(cleaned_data, 'password_new')
        password_new_again = dict_get(cleaned_data, 'password_new_again')
        if password_new != password_new_again:
            self._errors["password"] = self.error_class([u"两次密码输入不一致"])
        return cleaned_data



