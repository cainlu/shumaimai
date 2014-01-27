#coding=utf-8

import datetime 

TAXONOMY_DICT = {
    "航运与交通运输":u"航运与交通运输",
    "经济金融":u"经济金融",
    "工商管理":u"工商管理",
    "艺术设计":u"艺术设计",
    "法律":u"法律、语言、人文社科",
    "语言":u"法律、语言、人文社科",
    "人文社科":u"法律、语言、人文社科",
    "计算机科学":u"计算机与信息科学",
    "自然科学":u"自然科学",
    "工程机械":u"工程机械",
    "考试教辅":u"考试教辅",

    "自我管理":u"自我管理",
    "散文小说":u"散文小说",
    "杂文小说":u"散文小说",
    "趣味科学":u"趣味科学",
    "人物传记":u"人物传记",
    "阅读经典":u"阅读经典",
    "畅销图书":u"畅销图书",
    "吃喝玩乐":u"吃喝玩乐",
}



def str_format(i=None, null=False, blank=False, default=None): 
    try: 
        res = str(i)
        if res == '' and not blank:
            raise
        else:
            return res
    except:
        res = default
    if i is None:
        if null: return None 
        else: 
            raise

def int_format(i=None, null=False, default=None):
    try:
        i = i.strip()
    except:
        pass
    try:
        o = int(i)
    except:
        o = default
    if o is None:
        if null:
            return None
        else:
            raise
    else:
        return o

def float_format(i=None, null=False, default=None):
    try:
        i = i.strip()
    except:
        pass
    try:
        o = float(i)
    except:
        o = default
    if o is None:
        if null:
            return None
        else:
            raise
    else:
        return o

def date_format(i=None, null=False, default=None):
    try:
        i = i.split('/')
        year=int_format(i[0],False,2012)
        month=int_format(i[1],False,1)
        day=int_format(i[2],False,1)
        o = datetime.date(
                year=year,
                month=month,
                day=day
                )
    except Exception, e:
        o = default
    if o is None:
        if null:
            return None
        else:
            raise
    else:
        return o

def book_item_format(cvs_line=''):
    try:
        tmp = cvs_line.replace(' ', '')
        tmp = tmp.replace('?', '')
        tmp = tmp.replace('"', '')
        tmp = tmp.replace('、', ',')
        l = tmp.split('\t')
    except Exception, e:
        print e
        raise Exception("Par error.")
    length = len(l)
    if length < 15:
        for i in range(length, 15):
            l.append("")
    l[0] = str_format(l[0])
    l[1] = str_format(l[1])
    l[2] = str_format(l[2])
    l[3] = str_format(l[3])
    l[4] = float_format(l[4], default=0)
    l[5] = float_format(l[5], default=0)
    l[6] = str_format(l[6], null=True, blank=True)
    l[7] = int_format(l[7], null=True)
    l[8] = date_format(l[8], null=True, default=datetime.datetime.now().date())
    l[9] = int_format(l[9], null=True)
    l[10] = str_format(l[10], null=True, blank=True)
    l[11] = str_format(l[11], null=True)
    l[12] = str_format(l[12], default="zh")
    l[13] = str_format(l[13])
    l[14] = str_format(l[14])
    for i in l:
        if i != '':
            return l
    else:
        return []

def book_format(raw_data):
    raw_data = raw_data.replace('\r', '')
    raw_l = raw_data.split('\n')
    res_l = list()
    for i in raw_l:
        try:
            r = str(unicode(i, "gbk").encode('utf-8'))
        except Exception, e:
            try:
                r = str(i)
            except Exception, e:
                print "Book item encode error. Line number: " + str(raw_l.index(i))
                print i
                print e
                continue
        try:
            tmp_l = book_item_format(r)
        except Exception, e:
            print "Book item info error. Line number: " + str(raw_l.index(i))
            print e
            print i
            continue
        if tmp_l != list():
            res_l.append(tmp_l)
    return res_l

def book_input_auto():
    book_list = get_data('book_out.txt')
    from book.models import Book
    from book.models import Taxonomy
    
    for b in book_list:
        bs = None
        if b[6] != '':
            bs = Book.objects.filter(isbn=b[6]) 
        if bs is None or not bs.exists():
            bs = Book.objects.filter(name=b[0], version=b[7]) 
            if not bs.exists():
                try:
                    book = Book()
                    book.name = b[0]
                    book.subtitle = b[1]
                    if b[2] is None:
                        book.author = ''
                    else:
                        book.author = b[2]
                    if b[3] is None:
                        book.press = ''
                    else:
                        book.press = b[3]
                    book.price_ori = b[4]
                    if b[5] is None or b[5] == 0:
                        book.price_now = 0.4*b[4]
                    else:
                        book.price_now = b[5]
                    book.isbn = b[6]
                    book.version = b[7]
                    book.publication_date = b[8]
                    book.page_number = b[9]
                    book.size = b[10]
                    book.binding = b[11]
                    if b[12] == 'zh':
                        book.language = 'zh'
                    else:
                        book.language = 'en'
                    if b[13] is None:
                        book.translator = ''
                    else:
                        book.translator = b[13]
                    book.status = 4
                    book.save()
                    try:
                        if b[14] is not None and b[14] != '':
                            t = Taxonomy.objects.get(name=TAXONOMY_DICT[b[13]])
                            book.add_taxonomy(t)
                    except Exception, e:
                        print "Add taxonomy failed"
                        print e
                        print book_list.index(b)
                        print b
                        import pdb;pdb.set_trace()
                except Exception, e:
                    print e
                    print book_list.index(b)
                    print b

def get_data(f_name='data.txt'):
    f = open(f_name)
    raw_data = f.read()
    f.close()
    return book_format(raw_data)


if __name__ == "__main__":
    data = get_data('book_out.txt')
    import pdb;pdb.set_trace()
    print len(data)
    print data[97][13]





