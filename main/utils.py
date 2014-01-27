#coding=utf-8

import datetime
import unicodedata
import re 
import json
import datetime


def date_to_str(dt):
    try:
        return dt.strftime('%Y-%m-%d')
    except:
        return None

def datetime_to_str(dt):
    try:
        return dt.strftime('%Y-%m-%dT%H:%M:%S')
    except:
        return None

def my_json_dumps(obj):
    if isinstance(obj, datetime.datetime):
        return datetime_to_str(obj)
    elif isinstance(obj, datetime.date):
        return date_to_str(obj)
    else:
        raise TypeError('%r is not JSON serializable' % obj)

def my_ceil(fl):
    i = int(fl)
    if i < fl <= i + 0.5:
        return i + 0.5
    elif i + 0.5 < fl < i + 1:
        return i + 1.0
    else:
        return fl

def is_cn_char(char):
    return 0x4e00<=ord(char)<0x9fa6

def int_min(*args):
    res = None
    if len(args) > 0:
        for i in args:
            try:
                i = int(i)
                if res is None or res > i:
                    res = i
            except:
                pass
    return res

def choices_add_blank(choices):
    """ add one blank choices to data """
    tmp = list(choices)
    tmp.insert(0, ("", u''))
    return tuple(tmp)

def normalize_email(email):
    """
    Normalize the address by lowercasing the domain part of the email
    address.
    """
    email = email or ''
    try:
        email_name, domain_part = email.strip().rsplit('@', 1)
    except ValueError:
        pass
    else:
        email = '@'.join([email_name, domain_part.lower()])
    return email

def url_standard(url):
    if isinstance(url,list):
        res = list()
        for u in url:
            res.append(url_standard(u))
        return res
    elif url is not None:
        url = str(url)
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        if not url.endswith('/'):
            url = url + '/'
        return url

def url_link(*args):
    tmp = list()
    for i in args:
        tmp += i.split('/')
    tmp = list_standard(tmp)
    res = '/'.join(tmp)
    res = res.replace(':/', '://')
    return res

def dict_get(data_dict, name, default=None):
    if type(name) is list:
        res = {}
        for i in list_standard(name):
            try:
                res[i] = data_dict[i]
            except:
                if not default is None:
                    res[i] = default
        return res
    else:
        try:
            return data_dict[name]
        except:
            return default

def dict_remove_none(data_dict):
    """ remove None or "" in the dict """
    if (not data_dict is None) and (type(data_dict) == dict):
        for k in data_dict.keys():
            if data_dict[k] is None or data_dict[k] == "":
                del data_dict[k]
    return data_dict

def get_request_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def request_get(request, name, default=None, list_allowed=True, all_positive=False):
    res = request.GET.get(name)
    try:
        res = res.encode('utf-8')
        res = res.strip()
        res = res.replace('\'', '"')
        res = json.loads(res)
    except Exception, e:
        pass
    return par_standard(res, default, list_allowed, all_positive)

def par_standard(par, default=None, list_allowed=True, all_positive=False):
    res = par
    try:
        res = res.encode('utf-8').strip()
    except:
        pass
    try:
        res = res.strip()
    except:
        pass
    if res is None or res == '':
        return default
    elif type(res)==str:
        res = list_standard(res.split(','), all_positive)
    elif type(res)==int:
        if all_positive and res < 1:
            res = default
        res = [res] 
    elif isinstance(res, list) or isinstance(res, tuple) or isinstance(res, set):
        res = list(res)
    else:
        res = [res]
    if list_allowed:
        return res
    else:
        if len(res) <= 0:
            return default
        elif len(res) == 1:
            return res[0]
        else:
            return ','.join(res)

def to_datetime(string):
    if string is None:
        return None
    string = str(string).lower()
    sl = string.split("t")
    if len(sl) > 2:
        return None
    l = list()
    tmp = sl[0].split('-')
    if len(tmp) == 3:
        l += tmp
    else:
        return None
    try:
        tmp = sl[1].split(':')
        if len(tmp) >3:
            raise
        else:
            tmp[2] = tmp[2][:-1]
            l += tmp
    except:
        pass
    len_l = len(l)
    if len_l < 3 or len_l > 7:
        return None
    res = list()
    for i in l:
        try:
            res.append(int(i))
        except:
            pass
    try:
        d = datetime.datetime(*res)
    except Exception, e:
        print e
        d = None
    return d
 
def list_standard(l, all_positive=True):
    for i in range(0, len(l)):
        item = l[i]
        try:
            item = item.lower().strip()
        except:
            pass
        try:
            item = int(item)
            if all_positive:
                if item < 1:
                    item = ''
            else:
                if item < 0:
                    item = ''
        except:
            pass
        l[i] = item
    while(True):
        try:
            l.remove('')
        except:
            break
    return l

def alias_standard(alias):
    p1 = re.compile("[^-\dabcdefghijklmnopqsrtuvwxyz]+")
    p2 = re.compile('-+')
    res = alias.strip().lower().replace(' ', '-')
    res = re.sub(p1, '', res)
    res = re.sub(p2, '-', res)
    if res.startswith('-'):
        res = res[1:]
    if res.endswith('-'):
        res = res[:-1]
    return res

def alias_is_standard(alias):
    p1 = re.compile("^[-\dabcdefghijklmnopqsrtuvwxyz]+$")
    p2 = re.compile("(--)+")
    if re.match(p1, alias):
        if re.search(p2, alias):
            return False
        elif alias.startswith('-'):
            return False
        elif alias.endswith('-'):
            return False
        else:
            return True
    else:
        return False

def blank_standard(string):
    """ 
    return the string with standard blanks 
    blank standard:
        no blank at the start or end of the string
        no more than one blank between characters
    e.g.: 
        ' aaa     a    a a ' -> 'aaa a a a'
    """
    output = ""
    for item in string.strip().split(' '):
        if(item!=""):
            output += item + " "
    return output.strip()



