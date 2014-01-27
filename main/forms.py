#coding=utf-8

import logging

from django import forms

from utils import *

class BasicForm(forms.Form):

    _logger = logging.getLogger('default')

    def clean(self):
        cleaned_data = super(BasicForm, self).clean()
        return dict_remove_none(cleaned_data)


class BasicModelForm(forms.ModelForm):

    _logger = logging.getLogger('default')

    def clean(self):
        cleaned_data = super(BasicModelForm, self).clean()
        return dict_remove_none(cleaned_data)

