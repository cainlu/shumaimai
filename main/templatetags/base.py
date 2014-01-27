#coding=utf-8

import datetime

from django_jinja.base import Library
from django.core.urlresolvers import reverse

import jinja2, urllib

from main.utils import *

register = Library()

try:
    page_range_len = int(settings.DEFAULT_ADMIN_PAGE_RANGE_LENGTH)
except:
    page_range_len = 5


@register.global_function
def brief(text, max_length):
    try:
        length = int(max_length)
        j = 0
        for i in range(0,len(text)):
            j += 1
            if is_cn_char(text[i]):
                j += 1
            if j>length:
                text = text[:i-1] + "..."
                break
    except:
        pass
    return text

@register.global_function
def string(*args):
    res = ""
    for i in args:
        res += str(i)
    res = res.replace('&', '&amp;')
    replace_dict = {
            '"':'&quot;',
            ' ':'&nbsp;',
            '<':'&lt;',
            }
    for (key, value) in replace_dict.items():
        res = res.replace(key, value)
    return res


@register.global_function
def with_text_style(text, auto_indent=0):
    res = text
    auto_indent_text = int(auto_indent) * '&nbsp;'
    res = res.replace(' ', '&nbsp;')
    res = auto_indent_text + res
    res = res.replace('\n', '<br>' + auto_indent_text)
    return res

@register.global_function
def discount(price1, price2):
    if price2 == 0 and price2 == 0:
        res = 0
    elif price1 < price2:
        res = price1/price2
    else:
        res = price2/price1
    s_res = str(res*10)
    if len(s_res) > 3:
        return s_res[:3]
    else:
        return s_res

@register.global_function
def url_decode(url):
    url = url.encode('utf-8')
    par_dict = dict()
    raw_list = url.split('?')
    len_raw_list = len(raw_list)
    if len_raw_list > 2:
        raise Exception("Illegal url: too many '?'.")
    elif len_raw_list == 2:
        raw_pars_list = raw_list[1].split('&')
        for raw_par in raw_pars_list:
            par = urllib.unquote_plus(raw_par)
            try:
                tmp_list = par.split('=')
                par_dict[tmp_list[0]] = tmp_list[1]
            except:
                pass
    elif len_raw_list == 1:
        pass
    else:
        raise Exception("Illegal url: split error, length < 1.")
    return raw_list[0], par_dict

@register.global_function
def url_encode(url, par_add=False, **kwargs):
    if kwargs is not None and kwargs != dict():
        basic_url, par_dict = url_decode(url)
        if par_add:
            for k,v in kwargs.items():
                try:
                    vl = v.split(',')
                    try:
                        par_vl = par_dict[k].split(',')
                    except:
                        par_vl = []
                    res_vl = list(set(vl+par_vl))
                    kwargs[k] = ','.join(res_vl)
                except Exception, e:
                    print e
        par_dict.update(kwargs)
        res_par_dict = dict_remove_none(par_dict)
        get_data_dict = urllib.urlencode(res_par_dict.items())
        res_url = basic_url + '?' + get_data_dict
    else:
        res_url = url
    return res_url

@register.global_function
def url_par_remove(url, *args):
    res_url = url
    if args is not None and args != list():
        basic_url, par_dict = url_decode(url)
        for i in args:
            try:
                del par_dict[i]
            except Exception, e:
                pass
        res_url = url_encode(basic_url, **par_dict)
    return res_url

@register.global_function
def url_par_value_remove(url, par_name, par_value):
    res_url = url
    basic_url, par_dict = url_decode(url)
    try:
        par_value = urllib.urlencode({'':par_value})[1:]
        v = par_dict[par_name]
        vs = v.split(',')
        del vs[vs.index(str(par_value))]
        res_v = ','.join(vs)
        res_url = url_encode(url, **{par_name:res_v})
    except Exception, e:
        print e
    return res_url

@register.global_function
def url_get(url, arg):
    if arg is not None and arg != '':
        raw_url, par_dict = url_decode(url)
        try:
            return par_dict[arg]
        except:
            pass
    return ''

@register.global_function
def dict_add(*args):
    res = dict()
    for d in args:
        try:
            res.update(d)
        except:
            pass
    return res


@register.global_function
def get_page_range(cur, mn, mx):
    res_min = max(mn, cur - page_range_len + 1)
    res_max = min(mx, cur + page_range_len)
    if res_min == mn:
        if res_max != mx:
            res_max = min(mx, res_min + 2 * page_range_len - 1)
    elif res_max == mx:
        if res_min != mn:
            res_min = max(mn, res_max - 2 * page_range_len + 1)
    return res_min, res_max

@register.global_function
def is_instance(tar, t):
    return isinstance(tar, eval(str(t)))

@register.global_function
def out_link(link):
    if link is not None and link != '' and not link.startswith('http://'):
        link = 'http://' + link
    return link


@register.global_function
def now():
    return datetime.datetime.now().isoformat()

@register.global_function
def getint(value):
    return int(value)

@register.global_function
def get_day(value):
    return str(value)[:10]

@register.global_function
def get_split(stri, cut):
    return stri.split(cut)

@register.global_function
def text_replace(value):
    value = value.replace('\n', '<br>').replace('　　　', '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
    value = value.replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
    return value
