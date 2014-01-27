#coding=utf-8

import urllib
import urllib2
import re
import os
import datetime
import time
import xml.dom.minidom

class Dangdang(object):

    po1 = re.compile('<a[^>]*>[^<>]*</a>')
    po2 = re.compile('>[^<>]*<')

    p1 = re.compile('javascript:(AddToShoppingCart\(\d{3,}\))|(goto_product\(\d{3,}\))|(AddPDNothing\(\d{3,}\))')
    p2 = re.compile('\d+')

    p3 = re.compile('wsrc="http://.+\.jpg"')

    p4 = re.compile('<span class="c1">.{5,10}\d{4}-\d{1,2}-\d{1,2}.{,5}</span>')
    p5 = re.compile('\d{4}-\d{1,2}-\d{1,2}')

    p6 = re.compile('span class="c3"><span class="ws2">\xbf\xaa \xb1\xbe\xa3\xba</span>.{,7}</span>')
    p7 = re.compile('span class="c3"><span class="ws2">\xb0\xfc \xd7\xb0\xa3\xba</span>.{,7}</span>')
    p8 = re.compile('span class="c3"><span class="ws2">\xd2\xb3 \xca\xfd\xa3\xba</span>.{,7}</span>')
    p19 = re.compile('span class="c3"><span class="ws2">\xb0\xe6 \xb4\xce\xa3\xba</span>.{,7}</span>')
    p20 = re.compile('span class="c3"><i class="ws4">I S B N\xa3\xba</i>\d*</span>')

    p9 = re.compile('<i class="m_price">.{,10}</i>')

    p10 = re.compile('<h1>.+</h1>')
    p23 = re.compile('\([^\(]*http://.*\)')
    p11 = re.compile('<span class="c1"><span class="ws2">\xd7\xf7 \xd5\xdf\xa3\xba</span>.+</span>')

    p14 = re.compile('\xd6\xf8.*<a .+>.*</a>.*\xd2\xeb')
    p15 = re.compile('>.*</a>.*\xd2\xeb')

    p16 = re.compile('<span class="c1"><span class="ws1">\xb3\xf6 \xb0\xe6 \xc9\xe7\xa3\xba</span>.+</span>')
    p17 = re.compile('<a .+>.*</a>')
    p18 = re.compile('>.*</a>')

    @classmethod
    def _filter_tag_a_content(cls, text):
        res_list = list()
        res_l = re.findall(cls.po1, text)
        for res in res_l:
            tmp = re.findall(cls.po2, res)[0].decode('gbk').encode('utf-8')
            res_list.append(tmp[1:-1])
        return res_list

    @classmethod
    def _get_first_link_from_search_page(cls, raw):
        try:
            res_l = re.findall(cls.p1, raw)
            id = re.findall(cls.p2, ''.join(list(res_l[0])))[0]
            url = 'http://product.dangdang.com/product.aspx?product_id=' + str(id)
            return url
        except Exception, e:
            print e
            return None

    @classmethod
    def get_book_url_by_keywords(cls, key):
        search_url = 'http://searchb.dangdang.com/?' + urllib.urlencode({'key':key[:20]})# + '&category_path=01.00.00.00.00.00'
        print search_url
        try:
            time.sleep(2)
            raw = urllib2.urlopen(search_url, timeout=10).read()
        except Exception, e:
            print e
            print "Blocked! Start to sleep 61s!"
            time.sleep(31)
            raw = urllib2.urlopen(search_url, timeout=10).read()
        return cls._get_first_link_from_search_page(raw)
        return cls._get_first_link_from_search_page(raw)

    @classmethod
    def get_book_url_by_isbn(cls, isbn):
        search_url = 'http://searchb.dangdang.com/index.php?key1=&key4=' + str(isbn) + '&key2=&key3=&category_path=01.00.00.00.00.00&medium=01'
        print search_url
        try:
            time.sleep(2)
            raw = urllib2.urlopen(search_url, timeout=10).read()
        except Exception, e:
            print e
            print "Blocked! Start to sleep 61s!"
            time.sleep(31)
            raw = urllib2.urlopen(search_url, timeout=10).read()
        return cls._get_first_link_from_search_page(raw)

    @classmethod
    def get_book_html_by_target_url(cls, book_url):
        if book_url is not None and book_url != '':
            try:
                time.sleep(6)
                return urllib2.urlopen(book_url, timeout=10).read()
            except Exception, e:
                print e
                print "Blocked! Start to sleep 61s!"
                time.sleep(61)
                return urllib2.urlopen(book_url, timeout=10).read()
        else:
            raise Exception('Book Url is None.')

    @classmethod
    def filter_book_name(cls, text):
        res_l = list(set(re.findall(cls.p10, text)))
        if len(res_l) > 0:
            res = res_l[0][4:-46].replace('\xa3\xa8', '(').replace('\xa3\xa9', ')')
            tmp_l = list(set(re.findall(cls.p23, res)))
            for tmp in tmp_l:
                res = res.replace(tmp, '')
            return res.decode('gbk').encode('utf-8')
        else:
            return ''

    @classmethod
    def filter_book_isbn(cls, text):
        res_l = list(set(re.findall(cls.p20, text)))
        if len(res_l) > 0:
            return int(res_l[0][44:-7].decode('gbk').encode('utf-8'))
        else:
            return ''

    @classmethod
    def filter_book_author_and_translator(cls, text):
        res_l = list(set(re.findall(cls.p11, text)))
        if len(res_l) > 0:
            raw = res_l[0]
            raw_l = raw.split('\xd6\xf8')
            if len(raw_l) < 0:
                raw_l = raw.split('\xb1\xe0')
            author_str = raw_l[0]
            try:
                translator_str = raw_l[1]
            except:
                translator_str = None
            authors = cls._filter_tag_a_content(author_str)
            if translator_str is None:
                translators = list()
            else:
                translators = cls._filter_tag_a_content(translator_str)
            return authors, translators
        return list(), list()

    @classmethod
    def filter_book_img_url(cls, text):
        res_l = list(set(re.findall(cls.p3, text)))
        if len(res_l) > 0:
            return res_l[0][6:-1]
        else:
            return ''

    @classmethod
    def filter_book_press(cls, text):
        res_l = list(set(re.findall(cls.p16, text)))
        if len(res_l) > 0:
            raw = res_l[0]
            res_l = list(set(re.findall(cls.p17, raw)))
            if len(res_l) > 0:
                raw = res_l[0]
                res_l = list(set(re.findall(cls.p18, raw)))
                if len(res_l) > 0:
                    try:
                        return res_l[0][1:-4].decode('gbk').encode('utf-8').strip()
                    except:
                        pass
        return ''

    @classmethod
    def filter_book_version(cls, text):
        res_l = list(set(re.findall(cls.p19, text)))
        if len(res_l) > 0:
            return res_l[0][48:-7].decode('gbk').encode('utf-8')
        else:
            return ''

    @classmethod
    def filter_book_size(cls, text):
        res_l = list(set(re.findall(cls.p6, text)))
        if len(res_l) > 0:
            return res_l[0][48:-7].decode('gbk').encode('utf-8')
        else:
            return ''

    @classmethod
    def filter_book_binding(cls, text):
        res_l = list(set(re.findall(cls.p7, text)))
        if len(res_l) > 0:
            return res_l[0][48:-7].decode('gbk').encode('utf-8')
        else:
            return ''
    
    @classmethod
    def filter_book_page_number(cls, text):
        res_l = list(set(re.findall(cls.p8, text)))
        if len(res_l) > 0:
            return int(res_l[0][48:-7].replace('\xd2\xb3', ''))
        else:
            return 0
    
    @classmethod
    def filter_book_price_ori(cls, text):
        res_l = list(set(re.findall(cls.p9, text)))
        if len(res_l) > 0:
            p_str = res_l[0][24:-4]
            return float(p_str)
        else:
            return 0.0

    @classmethod
    def filter_book_publication_date(cls, text):
        res_l = list(set(re.findall(cls.p4, text)))
        if len(res_l) > 0:
            raw_dt = re.findall(cls.p5, res_l[0])[0]
            dt_l = raw_dt.split('-')
            dt = datetime.date(int(dt_l[0]), int(dt_l[1]), int(dt_l[2]))
            return dt
        else:
            return None

    @classmethod
    def get_img_by_url(cls, img_url, file_path):
        f = open(file_path, 'wb')
        try:
            raw = urllib2.urlopen(img_url, timeout=10).read()
        except Exception, e:
            print e
            print "Blocked! Start to sleep 61s!"
            time.sleep(61)
            raw = urllib2.urlopen(img_url, timeout=10).read()
        f.write(raw)
        f.close()


class Douban(object):

    ROOT = 'http://api.douban.com/book/subject/isbn/'
    API_KEY = '0cc4ab4b32942419264e01e197bc6c4b'

    @classmethod
    def filter_desc(cls, text):
        res = ''
        doc = xml.dom.minidom.parseString(text)
        for node in doc.getElementsByTagName("summary"):
            res += node.firstChild.nodeValue
        return res

    @classmethod
    def get_info_from_douban_by_isbn(cls, isbn):
        isbn = str(isbn)
        con = urllib.urlopen(cls.ROOT + isbn + '?apikey=' + cls.API_KEY).read()
        return con

