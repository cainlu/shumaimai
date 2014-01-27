#coding=utf-8

import logging

from django.contrib import auth
from django.forms.util import *

from widgets import *

from book.utils import *
from main.forms import *
from utils import *

def get_taxonomy():
    from book.models import Taxonomy
    res = list()
    t1s = Taxonomy.objects.filter(level=1)
    for t1 in t1s:
        t2s = t1.get_children()
        tmp = [ (t.id, t.name) for t in t2s ]
        res.append((t1.name, tuple(tmp)))
    return tuple(res)

TAXONOMY = get_taxonomy()

class BasicAdminForm(BasicForm):

    def as_bs_horizontal_form(self):
        res = ''
        try: res += u'<div class="text-error" style="padding-left:50px;">' + str(self.errors['__all__']) + '</div><br>'
        except:
            pass
        for name, field in self.fields.items():
            if not isinstance(self.fields[name].widget, forms.HiddenInput):
                if self[name].errors:
                    res += u'<div class="control-group error">'
                else:
                    res += u'<div class="control-group">'
                res += str(self[name].label_tag(attrs={"class":"control-label"}))
                res += u'<div class="controls">'
                res += str(self[name])
                res += u'<span class="help-inline">' + str(self[name].errors.as_text()) + '</span>'
                res += u'<span class="help-block">' + str(self[name].help_text) + '</span>'
                res += u'</div>'
                res += u'</div>'
            else:
                res += str(self[name])
        return res

class AdminLoginForm(BasicAdminForm):
    username = forms.CharField(label=u"用户名", max_length=30, required=True)
    password = forms.CharField(label=u"密码", max_length=30, required=True, widget=forms.PasswordInput)
    callback = forms.CharField(label=u"Callback", max_length=100, required=False, widget=forms.HiddenInput)

    def clean(self):
        try:
            clean_data = super(AdminLoginForm, self).clean()
            if self.errors:
                raise Exception("Nothing")
            username = dict_get(clean_data, 'username')
            password = dict_get(clean_data, 'password')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active and user.is_staff:
                clean_data['user'] = user
                return clean_data
            else:
                raise Exception("User illegal.")
        except Exception, e:
            raise forms.ValidationError("请输入正确的用户名密码。区分大小写。") 


class BookEditForm(BasicAdminForm):
    name = forms.CharField(label="书名", widget=forms.TextInput(attrs={"class":"input-xxlarge"}))
    subtitle = forms.CharField(label="副标题", widget=forms.TextInput(attrs={"class":"input-xxlarge"}), required=False)
    author = forms.CharField(label="作者")
    translator = forms.CharField(label="译者", required=False)
    isbn = forms.IntegerField(label="ISBN")
    press = forms.CharField(label="出版社")
    price_old = forms.FloatField(label="现价")
    price_ori = forms.FloatField(label="原价")
    status = forms.ChoiceField(
            label="状态", 
            widget=forms.Select(attrs={"class":"bs-select-deselect"}), 
            choices=BOOK_STATUS_CHOICES
            )
    publication_date = forms.DateTimeField(label="出版日期", widget=BSDateTimeInput, required=False)
    version = forms.CharField(label="版本", required=False)
    language = forms.ChoiceField(
            label="语言", 
            widget=forms.Select(attrs={"class":"bs-select-deselect"}), 
            choices=BOOK_LANGUAGE_CHOICES
            )
    page_number = forms.IntegerField(label="页数", required=False)
    size = forms.CharField(label="开本", required=False)
    binding = forms.CharField(label="装帧", required=False)

    taxonomy = forms.MultipleChoiceField(
            label="分类", 
            widget=forms.SelectMultiple(attrs={"class":"input-xxlarge bs-select"}), 
            choices=TAXONOMY, 
            required=False
            )

    description = forms.CharField(
            label=u"描述", 
            widget=forms.Textarea(attrs={"rows":10,"class":"input-xxlarge"}), 
            required=False
            )



class BookISBNAddForm(BasicAdminForm):
    isbn = forms.CharField(label=u"ISBN", max_length=30, required=True)

    def clean(self):
        clean_data = super(BookISBNAddForm, self).clean()
        if self.errors:
            return clean_data
        isbn = dict_get(clean_data, 'isbn')
        try:
            isbn = int(isbn)
            if isbn > 9999999999999 or isbn < 1000000000000:
                raise Exception('Nothing')
            clean_data['isbn'] = int(isbn)
        except:
            self.errors['isbn'] = ErrorList(["ISBN 必须是13 位数字!"])
        return clean_data

class OrderDownloadForm(BasicAdminForm):
    date = forms.DateField(label=u'日期', widget=BSDateInput, required=True)
    status_filterd = forms.BooleanField(label=u'仅未完成', required=False)


