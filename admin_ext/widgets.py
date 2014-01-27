#coding=utf-8

from django.forms import widgets
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode

class BSDateInput(widgets.DateTimeInput):
    
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            final_attrs['value'] = force_unicode(self._format_value(value))
        try:
            del final_attrs['data-date-format']
        except:
            pass
        final_attrs['data-date-format'] = self.format.split(' ')[0].replace('%Y', 'yyyy')\
                .replace('%m', 'mm').replace('%d', 'dd')
        html = u"""
        <div class="datepicker input-append date">
            <input%s />
            <span class="add-on"><i class="icon-remove"></i></span>
            <span class="add-on"><i class="icon-calendar"></i></span>
        </div>
        """ %flatatt(final_attrs)
        return mark_safe(html)



class BSDateTimeInput(widgets.DateTimeInput):
    
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            final_attrs['value'] = force_unicode(self._format_value(value))
        try:
            del final_attrs['data-date-format']
        except:
            pass
        final_attrs['data-date-format'] = self.format.replace('%Y', 'yyyy')\
                .replace('%m', 'mm').replace('%d', 'dd').replace('%H', 'hh')\
                .replace('%M', 'ii').replace('%S', 'ss')
        html = u"""
        <div class="datetimepicker input-append date">
            <input%s />
            <span class="add-on"><i class="icon-remove"></i></span>
            <span class="add-on"><i class="icon-calendar"></i></span>
        </div>
        """ %flatatt(final_attrs)
        return mark_safe(html)



