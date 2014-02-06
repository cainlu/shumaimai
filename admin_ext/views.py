#coding=utf-8

import os
import logging
import csv
import time

from django.conf import settings
from django.shortcuts import *
from django.core.paginator import *
from django.http import *
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.db import models
from django.core.exceptions import *

from forms import *
from decorators import *

from shopping.models import *
from logistic.models import *
from main.utils import *

time_interval = 43200
# Create your views here.

DEAL_FIELD_DICT = {
    'submittime':'submitTime',
    'deliverman':'deliverMan',
    'finishtime':'finishTime',
    'resultremark':'resultRemark',
    '-submittime':'-submitTime',
    '-deliverman':'-deliverMan',
    '-finishtime':'-finishTime',
    '-resultremark':'-resultRemark',
}

BOOK_STATUS = [ i[0] for i in Book._meta.get_field('status').get_choices() ]

def home(request):
    return render_to_response(
            'admin_ext/page/index.jinja', 
            {
            }, 
            RequestContext(request)
        )

def logout(request):
    request.user.get_profile().info_action(act='logout')
    auth.logout(request)
    return HttpResponseRedirect(reverse('admin_home'))

def login(request):
    if request.user.is_anonymous():
        try:
            refer = request.META['HTTP_REFERER']
            if refer == url_link('http://', request.get_host(), request.get_full_path()):
                raise
        except:
            refer = reverse('admin_home')
        if request.method == 'POST':
            login_form = AdminLoginForm(request.POST)
            if login_form.is_valid():
                data = login_form.cleaned_data
                user = dict_get(data, 'user')
                if user is not None:
                    auth.login(request, user)
                    user.get_profile().info_action(act='login')
                    callback = dict_get(data, 'callback', '').strip()
                    if len(callback) > 0:
                        target = refer
                    else:
                        target = callback
                    return HttpResponseRedirect(callback)
        else:
            login_form = AdminLoginForm(initial={'callback':refer})
        return render_to_response(
                'admin_ext/page/login.jinja', 
                {
                    'login_form':login_form
                },
                context_instance=RequestContext(request)
            )
    else:
        return HttpResponseRedirect(reverse('admin_home'))

@admin_auth_is_staff_required
def book_index(request):
    return render_to_response(
            'admin_ext/page/book_index.jinja', 
            {}, 
            RequestContext(request)
        )

@admin_auth_is_staff_required
def book_list(request):
    query = request_get(request, 'query', list_allowed=False)
    page = request_get(request, 'page', list_allowed=False)
    order = request_get(request, 'order', list())
    book_list = Book.objects.all()
    if query is not None:
        query = str(query)
        if query != "":
            q = models.Q(name__icontains=query) |\
                    models.Q(author__icontains=query) |\
                    models.Q(press__icontains=query) |\
                    models.Q(isbn__icontains=query)
            book_list = Book.objects.filter(q)
    book_list = book_list.order_by(*order)
    book_paginator = Paginator(book_list, settings.DEFAULT_NUM_PER_ADMIN_PAGE)
    try:
        books = book_paginator.page(page)
    except:
        books = book_paginator.page(1)
    return render_to_response(
            'admin_ext/page/book_list.jinja', 
            {
                'books':books,
                'query':query,
            }, 
            RequestContext(request)
        )

@admin_auth_is_staff_required
def admin_book_search(request):
    name = request_get(request, 'name', '', list_allowed=False)
    author = request_get(request, 'author', '', list_allowed=False)
    press = request_get(request, 'press', '', list_allowed=False)
    isbn = request_get(request, 'isbn', '', list_allowed=False)
    q = models.Q()
    if name != '':
        q = q | models.Q(name__icontains=name)
    if author != '':
        q = q | models.Q(author__icontains=author)
    if press != '':
        q = q | models.Q(press__icontains=press)
    if isbn != '':
        q = q | models.Q(isbn__icontains=isbn)
    book_list = Book.objects.filter(q)
    res = list()
    for book in book_list:
        res.append(
                {
                    'id':book.id,
                    'name':book.name,
                    'author':book.author,
                    'press':book.press,
                    'isbn':book.isbn
                }
            )
    return HttpResponse(json.dumps(res, default=my_json_dumps), mimetype="application/json")

@admin_auth_is_staff_required
def book_create(request):
    if request.method == 'POST':
        name = request.POST['name'].strip()
        author = request.POST['author'].strip()
        press = request.POST['press'].strip()
        isbn = request.POST['isbn'].strip()
        position = request.POST['position'].strip()
        control = int(request.POST['control'].strip())
        book = Book.objects.create(name=name, author=author, press=press, isbn=isbn, status=4)
        if position is not None and position != '':
            logistic = Logistic.objects.create(book=book, number=0, position=position)
        request.user.get_profile().info_action(act='create', msg='book id: ' + str(book.id))
        if control == 1:
            return HttpResponseRedirect(reverse('admin_book_list'))
        elif control == 2:
            return HttpResponseRedirect(reverse('admin_book_edit', kwargs={'id':book.id}))
    return HttpResponseRedirect(reverse('admin_home'))

@admin_auth_is_staff_required
def book_isbn_add(request):
    context = {'messages':list()}
    if request.method == 'POST':
        book_isbn_add_form = BookISBNAddForm(data=request.POST)
        if book_isbn_add_form.is_valid():
            data = book_isbn_add_form.cleaned_data
            try:
                isbn = data['isbn']
                book, created = Book.objects.get_or_create(isbn=isbn)
                if created:
                    book.status = 4
                    book.save()
                context['messages'].append({'type':'success','content':[u'成功添加。']})
                context['book'] = book
                return render_to_response(
                    'admin_ext/page/book_isbn_add_res.jinja', 
                    context, 
                    RequestContext(request)
                )
            except Exception, e:
                if isinstance(e, MultipleObjectsReturned):
                    context['messages'].append({'type':'error','content':[u'ISBN 重复。', u'请通过其他方式增加书籍。']})
                else:
                    logging.getLogger('default').error(str(e))
                    context['messages'].append({'type':'error','content':[u'未知错误。']})
    else:
        book_isbn_add_form = BookISBNAddForm()
    context['book_isbn_add_form'] = book_isbn_add_form
    return render_to_response(
        'admin_ext/page/book_isbn_add.jinja', 
        context, 
        RequestContext(request)
    )

@admin_auth_is_superuser_required
def order_index(request):
    return render_to_response(
            'admin_ext/page/order_index.jinja', 
            {}, 
            RequestContext(request)
        )

@admin_auth_is_superuser_required
def order_buy_list(request):
    query = request_get(request, 'query', list_allowed=False)
    page = request_get(request, 'page', list_allowed=False)
    o = request_get(request, 'order', list())
    order_list = Deal.objects.all()
    if query is not None:
        query = str(query)
        if query != "":
            q = models.Q(id__icontains=query) |\
                    models.Q(phone__icontains=query)
            order_list = Deal.objects.filter(q)
    res_o = list()
    for i in o:
        try:
            res_o.append(DEAL_FIELD_DICT[i])
        except:
            res_o.append(i)
    if res_o is None or res_o == list():
        res_o = ['-submitTime']
    order_list = order_list.order_by(*res_o)
    order_paginator = Paginator(order_list, settings.DEFAULT_NUM_PER_ADMIN_PAGE)
    try:
        orders = order_paginator.page(page)
    except:
        orders = order_paginator.page(1)
    return render_to_response(
            'admin_ext/page/order_buy_list.jinja', 
            {
                'orders':orders,
            }, 
            RequestContext(request)
        )

@admin_auth_is_superuser_required
def order_buy_edit(request, id):
    order = Deal.objects.get(id=id)
    return render_to_response(
        'admin_ext/page/order_buy_edit.jinja', 
        {
            'order':order,
        }, 
        RequestContext(request)
    )

@admin_auth_is_superuser_required
def order_buy_detail_set(request, id):
    price_buy= request_get(request, 'price-buy', list_allowed=False)
    price_sell = request_get(request, 'price-sell', list_allowed=False)
    try:
        detail = Book_Deal.objects.get(id=id)
        if price_buy is not None:
            request.user.get_profile().info_action(act='change', msg='order id: ' + str(id) + '\nprice_buy: ' + str(detail.price_buy) + ' -> ' + str(price_buy))
            detail.price_buy = float(price_buy)
        if price_sell is not None:
            request.user.get_profile().info_action(act='change', msg='order id: ' + str(id) + '\nprice_sell: ' + str(detail.price_sell) + ' -> ' + str(price_sell))
            detail.price_sell = float(price_sell)
        detail.save()
        msg = {'type':'success','content':u'操作成功。'}
    except Exception, e:
        print e
        msg = {'type':'error','content':u'操作时败。错误 -> '+str(e)}
    return HttpResponse(json.dumps(msg))

@admin_auth_is_superuser_required
def order_sell_list(request):
    query = request_get(request, 'query', list_allowed=False)
    page = request_get(request, 'page', list_allowed=False)
    o = request_get(request, 'order', list())
    res_o = list()
    order_list = Sell_Deal.objects.all()
    if query is not None:
        query = str(query)
        if query != "":
            q = models.Q(id__icontains=query) |\
                    models.Q(phone__icontains=query)
            order_list = Sell_Deal.objects.filter(q)
    for i in o:
        try:
            res_o.append(DEAL_FIELD_DICT[i])
        except:
            res_o.append(i)
    if res_o is None or res_o == list():
        res_o = ['-submitTime']
    order_list = order_list.order_by(*res_o)
    order_paginator = Paginator(order_list, settings.DEFAULT_NUM_PER_ADMIN_PAGE)
    try:
        orders = order_paginator.page(page)
    except:
        orders = order_paginator.page(1)
    return render_to_response(
            'admin_ext/page/order_sell_list.jinja', 
            {
                'orders':orders,
            }, 
            RequestContext(request)
        )

@admin_auth_is_superuser_required
def order_sell_edit(request, id):
    order = Sell_Deal.objects.get(id=id)
    return render_to_response(
        'admin_ext/page/order_sell_edit.jinja', 
        {
            'order':order,
        }, 
        RequestContext(request)
    )

@admin_auth_is_superuser_required
def order_buy_set(request):
    id_list = request_get(request, 'id', list())
    score = request_get(request, 'score', list_allowed=False)
    score_return = request_get(request, 'score-return', list_allowed=False)
    result_remark = request_get(request, 'result-remark', list_allowed=False)
    status = request_get(request, 'status', list_allowed=False)
    try:
        orders = Deal.objects.filter(id__in=id_list)
        for order in orders:
            if status is not None:
                status = int(status)
                if status in range(0,7):
                    request.user.get_profile().info_action(act='change', msg='buy order id: ' + str(id_list) + '\nstatus: ' + str(order.status) + ' -> ' + str(status))
                    if order.user is not None and order.user.get_profile() is not None:
                        profile = order.user.get_profile()
                        if status == 1:
                            profile.score = profile.score + order.score_return
                        elif status == 2:
                            profile.score = profile.score + order.score
                        profile.save()
                    order.status = status
                else:
                    raise Exception('订单状态必须在0-6')
            if score is not None and int(score) >= 0:
                request.user.get_profile().info_action(act='change', msg='buy order id: ' + str(id_list) + '\nscore: ' + str(order.score) + ' -> ' + str(score))
                if order.user is not None and order.user.get_profile() is not None:
                    profile = order.user.get_profile()
                    profile.score = profile.score + order.score - score
                    profile.save()
                order.score = score
            order.save()
            if result_remark is not None:
                request.user.get_profile().info_action(act='change', msg='buy order id: ' + str(id_list) + '\nresult_remark: ' + str(order.resultRemark) + ' -> ' + str(result_remark))
                order.resultRemark = result_remark
            if score_return is not None and int(score_return) >= 0:
                request.user.get_profile().info_action(act='change', msg='buy order id: ' + str(id_list) + '\nscore_return: ' + str(order.score_return) + ' -> ' + str(score_return))
                order.score_return = score_return
            order.save()
        msg = {'type':'success','content':u'操作成功。'}
    except Exception, e:
        print e
        msg = {'type':'error','content':u'操作时败。错误 -> '+str(e)}
    return HttpResponse(json.dumps(msg))

@admin_auth_is_superuser_required
def order_sell_set(request):
    id_list = request_get(request, 'id', list())
    price_all = request_get(request, 'price-all', list_allowed=False)
    result_remark = request_get(request, 'result-remark', list_allowed=False)
    status = request_get(request, 'status', list_allowed=False)
    try:
        orders = Sell_Deal.objects.filter(id__in=id_list)
        for order in orders:
            if status is not None:
                status = int(status)
                if status in range(0,7):
                    request.user.get_profile().info_action(act='change', msg='sell order id: ' + str(id_list) + '\nstatus: ' + str(order.status) + ' -> ' + str(status))
                    order.status = status
                else:
                    raise Exception('订单状态必须在0-6')
            if price_all is not None:
                request.user.get_profile().info_action(act='change', msg='sell order id: ' + str(id_list) + '\nprice_all: ' + str(order.price_all) + ' -> ' + str(price_all))
                order.price_all = price_all
            if result_remark is not None:
                request.user.get_profile().info_action(act='change', msg='buy order id: ' + str(id_list) + '\nresult_remark: ' + str(order.resultRemark) + ' -> ' + str(result_remark))
                order.resultRemark = result_remark
            order.save()
        msg = {'type':'success','content':u'操作成功。'}
    except Exception, e:
        print e
        msg = {'type':'error','content':u'操作时败。错误 -> '+str(e)}
    return HttpResponse(json.dumps(msg))

@admin_auth_is_superuser_required
def order_book_deal_delete(request):
    id_list = request_get(request, 'id', list())
    try:
        book_deals = Book_Deal.objects.filter(id__in=id_list)
        msg = ''
        for book_deal in book_deals:
            msg += 'book_deal id: ' + str(book_deal.id) +  '; ' + \
                    'book id: ' + str(book_deal.book.id) + '; ' + \
                    'book name: ' + str(book_deal.book.name) + '; ' + \
                    '\n'
        book_deals.delete()
        request.user.get_profile().info_action(act='delete', msg=msg)
        msg = {'type':'success','content':u'操作成功。'}
    except Exception, e:
        print e
        msg = {'type':'error','content':u'操作时败。错误 -> '+str(e)}
    return HttpResponse(json.dumps(msg))

@admin_auth_is_superuser_required
def order_download(request):
    context = {}
    if request.method == 'POST':
        order_download_form = OrderDownloadForm(data=request.POST)
        if order_download_form.is_valid():
            data = order_download_form.cleaned_data
            date = dict_get(data, 'date')
            status_filterd = dict_get(data, 'status_filterd')
            orders = Deal.objects.filter(
                    submitTime__year=date.year,
                    submitTime__month=date.month,
                    submitTime__day=date.day,
                    )
            if status_filterd:
                orders = orders.filter(status__in=[3, 4, 6])
            f_name = date.isoformat()
            response = HttpResponse(mimetype="text/csv")
            response['Content-Disposition'] = 'attachment; filename=' + f_name + '.csv'
            writer = csv.writer(response)
            writer.writerow([
                    '订单号'.encode('gbk'), 
                    '电话'.encode('gbk'), 
                    '地址'.encode('gbk'), 
                    '订单状态'.encode('gbk'), 
                    '书名'.encode('gbk'), 
                    '需求量'.encode('gbk'), 
                    '库位号'.encode('gbk'), 
                    '实发数量'.encode('gbk'), 
                    '单价'.encode('gbk'), 
                    '总价'.encode('gbk'), 
                    '状态'.encode('gbk')
                    ])
            for order in orders:
                for book_deal in order.get_book_deals():
                    book = book_deal.book
                    lgss = book.get_logistic_info()
                    lgs_info = [ lgs.position for lgs in lgss ]
                    writer.writerow([
                            order.id,
                            str(order.phone).encode('gbk'),
                            order.address.encode('gbk'),
                            order.get_status_display().encode('gbk'),
                            book.name.encode('gbk'),
                            book_deal.number,
                            ' '.join(lgs_info).encode('gbk'),
                            '',
                            book.price_old,
                            '',
                            '',
                            ])
            return response
    else:
        order_download_form = OrderDownloadForm(initial={'status_filterd':True})
    context['order_download_form'] = order_download_form
    return render_to_response(
            'admin_ext/page/order_download.jinja', 
            context,
            context_instance=RequestContext(request)
        )

@admin_auth_is_staff_required
def book_edit(request, id):
    context = {}
    order = request_get(request, 'order', list())
    book = Book.objects.get(id=id)
    context['book'] = book
    if order == list():
        order = ['id']
    context['messages'] = list()
    if request.method == 'POST':
        book_edit_form = BookEditForm(data=request.POST)
        if book_edit_form.is_valid():
            data = book_edit_form.cleaned_data
            try:
                control = int(dict_get(data, 'control'))
            except:
                control = 1
            try:
                book.name = dict_get(data, 'name')
                book.subtitle = dict_get(data, 'subtitle')
                book.author = dict_get(data, 'author', '')
                book.translator = dict_get(data, 'translator', '')
                book.isbn = dict_get(data, 'isbn')
                if book.isbn is not None:
                    book.isbn = int(book.isbn)
                book.press = dict_get(data, 'press', 0)
                book.price_old = dict_get(data, 'price_old', 0)
                book.price_ori = dict_get(data, 'price_ori', 0)
                book.status = dict_get(data, 'status', 0)
                book.publication_date = dict_get(data, 'publication_date')
                book.version = dict_get(data, 'version')
                if book.version is not None:
                    book.version = int(book.version)
                book.language = dict_get(data, 'language', 'zh')
                book.page_number = int(dict_get(data, 'page_number', 0))
                book.size = dict_get(data, 'size')
                book.binding = dict_get(data, 'binding')
                book.description = dict_get(data, 'description')
                book.save()
                request.user.get_profile().info_action(act='change', msg='book id: ' + str(book.id))
                ts_id_list = [ int(t) for t in dict_get(data,'taxonomy', list()) ]
                book.taxonomy_list = Taxonomy.objects.filter(id__in=ts_id_list)
                context['messages'].append({'type':'success','content':[u'book Change Success:', u'book id -> ' + str(book.id)]})
            except Exception, e:
                context['messages'].append({'type':'error','content':[u'Book Change Failed:', u'book id -> ' + str(book.id), u' Error -> '+ str(e)]})
        else:
            context['messages'].append({'type':'error','content':[u'Book Change Failed:', u'book id -> ' + str(book.id)]})
    else:
        ts_list = [ t.id for t in book.get_taxonomy() ]
        initial_data = {
                    'name':book.name,
                    'subtitle':book.subtitle,
                    'author':book.author,
                    'translator':book.translator,
                    'isbn':book.isbn,
                    'press':book.press,
                    'price_old':book.price_old,
                    'price_ori':book.price_ori,
                    'status':book.status,
                    'publication_date':book.publication_date,
                    'version':book.version,
                    'language':book.language,
                    'page_number':book.page_number,
                    'size':book.size,
                    'binding':book.binding,
                    'description':book.description,
                    'taxonomy':ts_list,
                }
        book_edit_form = BookEditForm(initial=initial_data)
    context['book'] = book
    context['book_edit_form'] = book_edit_form
    return render_to_response(
            'admin_ext/page/book_edit.jinja', 
            context,
            context_instance=RequestContext(request)
        )

@admin_auth_is_staff_required
def book_set(request):
    id_list = request_get(request, 'id', list())
    status = request_get(request, 'status', list_allowed=False)
    try:
        if status is not None and int(status) in BOOK_STATUS:
            Book.objects.filter(id__in=id_list).update(status=int(status))
            request.user.get_profile().info_action(act='change', msg='book id: ' + str(id_list) + '\nstatus: ' + str(status))
        msg = {'type':'success','content':u'操作成功。'}
    except Exception, e:
        print e
        msg = {'type':'error','content':u'操作时败。错误 -> '+str(e)}
    return HttpResponse(json.dumps(msg))

@admin_auth_is_staff_required
def book_change_cover(request, id):
    try:
        refer = request.META['HTTP_REFERER']
    except:
        refer = reverse('admin_home')
    try:
        if request.method == "POST":
            cover_in_memery = request.FILES['image']
            book = Book.objects.get(id=id)
            im_dict = book.image_dict
            im_dict['cover'] = os.path.join(settings.IMAGE_URL, 'book', str(book.id), 'cover.jpg')
            book.image_dict = im_dict
            im_dir_path = os.path.join(settings.IMAGE_ROOT, 'book', str(book.id))
            if not os.path.exists(im_dir_path):
                os.makedirs(im_dir_path)
            im_path = os.path.join(im_dir_path, 'cover.jpg')
            f = open(im_path, 'wb')
            f.write(cover_in_memery.read())
            f.close()
            book.save()
            request.user.get_profile().info_action(act='change', msg='book id: ' + str(id_list) + '\ncover')
            msg = {'type':'success','content':u'Cover change succeeded.'}
        else:
            raise Exception("Only post method is supported")
    except Exception, e:
        print e
        msg = {'type':'error','content':u'Cover change Failed. error -> '+str(e)}
    return HttpResponseRedirect(refer)

@admin_auth_is_staff_required
def logistic_set(request):
    id_list = request_get(request, 'id', list())
    number = request_get(request, 'number', list_allowed=False)
    try:
        number = int(number)
        for logistic in Logistic.objects.filter(id__in=id_list):
            request.user.get_profile().info_action(act='change', msg='logistic id: ' + str(id_list) + '\nnumber: ' + str(logistic.number) + ' -> ' + str(number))
            logistic.number = number
            logistic.save()
        msg = {'type':'success','content':u'操作成功。'}
    except Exception, e:
        print e
        msg = {'type':'error','content':u'操作时败。错误 -> '+str(e)}
    return HttpResponse(json.dumps(msg))

@admin_auth_is_staff_required
def logistic_add(request):
    book_id = request.POST['id'].strip()
    position = request.POST['position'].strip()
    try:
        logistics = Logistic.objects.create(book=Book.objects.get(id=int(book_id)), position=position, number=0)
        request.user.get_profile().info_action(act='add', msg='logistic id: ' + str(id_list) + '\nbook id: ' + str(book_id) + '\nposition: ' + str(position))
        msg = {'type':'success','content':u'操作成功。'}
    except Exception, e:
        print e
        msg = {'type':'error','content':u'操作时败。错误 -> '+str(e)}
    return HttpResponse(json.dumps(msg))

@admin_auth_is_staff_required
def logistic_delete(request):
    id_list = request_get(request, 'id', list())
    try:
        logistics = Logistic.objects.filter(id__in=id_list)
        msg = ''
        for logistic in logistics:
            msg += 'logistic id: ' + str(logistic) + '; ' + \
                    'book id: ' + str(logistic.book.id) + '; ' + \
                    'book name: ' + str(logistic.book.name) + '; ' +  \
                    'logistic position: ' + str(logistic.position) + '; ' +  \
                    '\n'
        logistics.delete()
        request.user.get_profile().info_action(act='delete', msg=msg)
        msg = {'type':'success','content':u'操作成功。'}
    except Exception, e:
        print e
        msg = {'type':'error','content':u'操作时败。错误 -> '+str(e)}
    return HttpResponse(json.dumps(msg))

@admin_auth_is_superuser_required
def order_pick_list(request):
    page = request_get(request, 'page', list_allowed=False)
    
    begin_time = '2013-01-01 00:00:00'
    begin_time = time.strptime(begin_time, '%Y-%m-%d %H:%M:%S')
    begin_time = int(time.mktime(begin_time))
    end_time = time.time()
    time_list = []
    while True:
        if begin_time > end_time:
            break
        time_list.append({'time_stamp':begin_time, 
                          'time_show':'%s到%s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(begin_time)), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(begin_time + time_interval)))})
        begin_time += time_interval
    time_list.reverse()
    order_paginator = Paginator(time_list, settings.DEFAULT_NUM_PER_ADMIN_PAGE)
    try:
        orders = order_paginator.page(page)
    except:
        orders = order_paginator.page(1)
    return render_to_response(
            'admin_ext/page/order_pick_list.jinja', 
            {
                 'orders':orders,
            }, 
            RequestContext(request)
        )

@admin_auth_is_superuser_required
def order_pick_show(request, time_stamp):
    time_stamp = int(time_stamp)
    begin_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_stamp))
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_stamp + time_interval))
    deals = Deal.objects.filter(submitTime__range=(begin_time, end_time)).exclude(status=7)
    book_nums = {}
    for deal in deals:
        book_deals = Book_Deal.objects.filter(deal_id=deal.id)
        for book_deal in book_deals:
            book_nums[book_deal.book_id] = book_nums.get(book_deal.book_id, 0) + 1
    books = Book.objects.filter(id__in = book_nums.keys())
    return render_to_response(
            'admin_ext/page/order_pick_show.jinja', 
            {
             'book_nums':book_nums, 'books':books, 'time_stamp':time_stamp,
            }, 
            RequestContext(request)
        )
    
@admin_auth_is_superuser_required
def order_pick_finish(request, time_stamp):
    time_stamp = int(time_stamp)
    begin_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_stamp))
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_stamp + time_interval))
    deals = Deal.objects.filter(submitTime__range=(begin_time, end_time)).exclude(status=7)
    for deal in deals:
        deal.status = 7
        deal.save()
    return HttpResponseRedirect('/admin-ext/order/pick/%s/' % time_stamp)
    