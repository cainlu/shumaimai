#coding=utf-8

def test():
    f = open('isbn_1.txt', 'rb')
    raw = f.read()
    f.close()
    ls = raw.replace('\r', '').split('\n')
    res = list()
    for ll in ls:
        tmp = str(unicode(ll, "gbk").encode('utf-8')).split('\t')
        if len(tmp) == 2:
            res.append(tmp)
    return res

def db_re(data):
    from book.models import Book
    mo_list = list()
    none_list = list()
    for da in data:
        bo = Book.objects.filter(name=da[0])
        if bo.count() > 1:
          mo_list.append(da)
        elif bo.count() <= 0:
          none_list.append(da)
        else:
          bo[0].isbn = da[1]
          bo[0].save()
    return mo_list, none_list

