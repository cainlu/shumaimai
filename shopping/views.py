#coding=utf-8

from django.http import *
from django.shortcuts import *
from django.core.mail import send_mail
from django.conf import settings
from book.models import *
from shopping.models import *
from account.models import *
from models import *
from PyWapFetion import *
from search.utils import *
from shopping.forms import SellForm
from django.views.decorators.cache import cache_page
import urllib
import time
import json

#下订单
def order(request):
    ip = request.META['REMOTE_ADDR']
    phone = request.POST['phone']
    address = request.POST['address']
    remark = request.POST['remark']
    score = request.POST['score']
    if (not score):
        score = '0'
    if (not phone) or (not address) or (not phone.isdigit()) or (not score.isdigit()):
        return render_to_response("page/index.jinja", {'message':u'&nbsp;&nbsp;&nbsp;非法操作'}, RequestContext(request))
    emailtext = ''
    not0 = 0
    typenum = 0
    urlnum = 0
    bookbehalfnum = 0
    newscore = 0
    tmpbookDic = {}
    dealid = int(time.strftime('%Y%m%d',time.localtime(time.time())) + '10001')
    try:
        maxid = int(Deal.objects.order_by('-id')[0].id)
        if maxid >= dealid:
            dealid = maxid + 1
    except Exception, e:
        print e
    if 'typenum' in request.COOKIES:
        typenum = int(request.COOKIES['typenum'])
        for i in range(typenum):
            tmpid = request.COOKIES['bookid' + str(i)]
            tmpname = request.COOKIES['bookname' + str(i)]
            tmpname = urllib.unquote(tmpname)
            tmpauthor = request.COOKIES['bookauthor' + str(i)]
            tmpauthor = urllib.unquote(tmpauthor)
            tmppublisher = request.COOKIES['bookpublisher' + str(i)]
            tmppublisher = urllib.unquote(tmppublisher)
            tmpisbn = request.COOKIES['bookisbn' + str(i)]
            tmpnum = request.COOKIES['booknum' + str(i)]
            if int(tmpnum) > 0:
                not0 += 1
                emailtext += tmpname + '###' + tmpauthor + '###' + tmppublisher + '###' + \
                                                                            tmpisbn + '###'+ tmpnum + '本\n'
                book = Book.objects.filter(id=tmpid)
                if len(book) <= 0:
                    return render_to_response("page/index.jinja", {'message':u'&nbsp;&nbsp;&nbsp;非法操作'}, RequestContext(request))
                newscore += book[0].price_old * int(tmpnum)
                tmpbookDic.update({tmpid:tmpnum})
    if 'urlbehalftotalnum' in request.COOKIES:
        urlnum = int(request.COOKIES['urlbehalftotalnum'])
        for i in range(urlnum):
            tmpnum = request.COOKIES['urlbehalfnum' + str(i)]
            if int(tmpnum) > 0:
                not0 += 1
    if 'bookbehalftotalnum' in request.COOKIES:
        bookbehalfnum = int(request.COOKIES['bookbehalftotalnum'])
        for i in range(bookbehalfnum):
            tmpnum = request.COOKIES['bookbehalfnum' + str(i)]
            if int(tmpnum) > 0:
                not0 += 1
    if not0 <= 0:
        return render_to_response("page/index.jinja", {'message':u'&nbsp;&nbsp;&nbsp;请先购买书籍'}, RequestContext(request))
    if '_auth_user_id' in request.session:
        user_id = request.session['_auth_user_id']
        user = User.objects.filter(id=user_id)
        if len(user) > 0:
            user = user[0]
            user_profile = UserProfile.objects.get(user_id=user_id)
            if int(score) <= user_profile.score:
                deal = Deal.objects.create(
                        id=dealid,
                        status=3,
                        address=address,
                        phone=phone,
                        remark=remark,
                        ip=ip,
                        user=user,
                        score=score,
                        )
            else:
                return render_to_response("page/index.jinja", {'message':u'&nbsp;&nbsp;&nbsp;积分不足'}, RequestContext(request))
    else:
        deal = Deal.objects.create(
            id=dealid,
            status=3,
            address=address,
            phone=phone,
            remark=remark,
            ip=ip,
            )
        if 'dealnum' in request.session:
            dealnum = request.session['dealnum']
            request.session['dealnum'] = int(dealnum) + 1
            request.session['deal' + str(dealnum)] = deal.id
        else:
            request.session['dealnum'] = 1
            request.session['deal0'] = deal.id
    if not deal:
        return render_to_response("page/index.jinja", {'message':u'&nbsp;&nbsp;&nbsp;订购错误'}, RequestContext(request))
    for i in tmpbookDic.keys():
        if i.isdigit():
            book_deal = Book_Deal.objects.create(
                                            book=Book.objects.get(id=i),
                                            number=tmpbookDic[i],
                                            deal=deal,
                                            type=1,
                                            )
            if not book_deal:
                return render_to_response("page/index.jinja", {'message':u'&nbsp;&nbsp;&nbsp;订购错误'}, RequestContext(request))
    for i in range(urlnum):
        tmpurl = request.COOKIES['url' + str(i)]
        tmpurl = urllib.unquote(tmpurl)
        tmpnum = request.COOKIES['urlbehalfnum' + str(i)]
        if int(tmpnum) > 0:
            url_deal = Book_Deal.objects.create(
                                                url=tmpurl,
                                                number=tmpnum,
                                                deal=deal,
                                                type=2,
                                                )
            if not url_deal:
                return render_to_response("page/index.jinja", {'message':u'&nbsp;&nbsp;&nbsp;订购错误'}, RequestContext(request))
    for i in range(bookbehalfnum):
        tmpname = request.COOKIES['bookbehalfname' + str(i)]
        tmpname = urllib.unquote(tmpname)
        tmpauthor = request.COOKIES['bookbehalfauthor' + str(i)]
        tmpauthor = urllib.unquote(tmpauthor)
        tmppublisher = request.COOKIES['bookbehalfpublisher' + str(i)]
        tmppublisher = urllib.unquote(tmppublisher)
        tmpisbn = request.COOKIES['bookbehalfisbn' + str(i)]
        tmpurl = request.COOKIES['bookbehalfurl' + str(i)]
        tmpnum = request.COOKIES['bookbehalfnum' + str(i)]
        if int(tmpnum) > 0:
            emailtext += tmpname + '###' + tmpauthor + '###' + tmppublisher + '###' + tmpisbn + \
                                                                                '###'+ tmpnum + '本（代购）\n'
            bookBehalf = Book.objects.filter(
                                    name=tmpname,
                                    author=tmpauthor,
                                    press=tmppublisher,
                                    isbn=tmpisbn,
                                    )
            if len(bookBehalf) == 0:
                bookBehalf = Book.objects.create(
                                                name=tmpname,
                                                author=tmpauthor,
                                                press=tmppublisher,
                                                isbn=tmpisbn,
                                                status=0,
                                                )
            else:
                bookBehalf = bookBehalf[0]
            book_behalf_deal = Book_Deal.objects.create(
                                            book=bookBehalf,
                                            url=tmpurl,
                                            number=tmpnum,
                                            deal=deal,
                                            type=3,
                                            )
            if not book_behalf_deal:
                return render_to_response("page/index.jinja", {'message':u'&nbsp;&nbsp;&nbsp;订购错误'}, RequestContext(request))
    if '_auth_user_id' in request.session:
        user_profile.score -= int(score)
        user_profile.save()
    newscore = int(newscore * settings.DEFAULT_SCORE_RETURN_RATE_PER_DEAL)
    deal.score_return = newscore
    deal.status = 3
    deal.save()
    emailtext += '备注：' + remark + '\n'
    emailtext += '积分：' + score + '\n'
    emailtext += '时间：' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '\n'
    emailtext += 'url：' + 'http://shumaimai.cn/admin-ext/order/buy/' + str(dealid) + '/edit/'
    send_mail('买书，电话：' + phone + '，地址：' + address + '，订单号：' + str(dealid), \
            emailtext, settings.DEFAULT_FROM_EMAIL, settings.DEFAULT_TO_EMAIL, )
    return render_to_response("page/index.jinja", {'page':'buy', 'dealid':deal.id, 'score':newscore,}, RequestContext(request))

#显示订单
def ordershow(request):
    #订单
    deals = {}
    if '_auth_user_id' in request.session:
        user_id = request.session['_auth_user_id']
        user = User.objects.get(id=user_id)
        tmpdeals = Deal.objects.filter(user_id=user).order_by('-submitTime')
        if len(tmpdeals) > 0:
            firstdeal = tmpdeals[0]
        else:
            firstdeal = ''
        for tmpdeal in tmpdeals:
            tmpdeal_dict = {}
            books = {}
            tmpdeal_dict['submitTime'] = tmpdeal.submitTime
            tmpdeal_dict['finishTime'] = tmpdeal.finishTime
            totalPrice = 0
            storePrice = 0
            book_deal = Book_Deal.objects.filter(deal_id=tmpdeal.id, book_id__isnull=False)
            for j in range(len(book_deal)):
                book = Book.objects.get(id=book_deal[j].book_id)
                books[book] = book_deal[j].number
                totalPrice += int(book_deal[j].number) * float(book.price_old)
                storePrice += int(book_deal[j].number) * float(book.price_ori)
            tmpdeal_dict['totalPrice'] = totalPrice
            tmpdeal_dict['savePrice'] = storePrice - totalPrice 
            tmpdeal_dict['books'] = books
            deals[tmpdeal] = tmpdeal_dict
        if len(deals) > 0:
            dealkeys = deals.keys()
            dealkeys.reverse()
            return render_to_response("page/ordershow.jinja", {'deals':deals, 'firstdeal':firstdeal, \
                                                            'dealkeys':dealkeys}, RequestContext(request))
        else:
            return render_to_response("page/ordershow.jinja", {}, RequestContext(request))
    elif 'dealnum' in request.session:
        dealnum = request.session['dealnum']
        for i in range(int(dealnum)):
            tmpdeal_dict = {}
            books = {}
            deal_id = request.session['deal' + str(i)]
            tmpdeal = Deal.objects.get(id=deal_id)
            tmpdeal_dict['submitTime'] = tmpdeal.submitTime
            tmpdeal_dict['finishTime'] = tmpdeal.finishTime
            totalPrice = 0
            storePrice = 0
            book_deal = Book_Deal.objects.filter(deal_id=deal_id, book_id__isnull=False)
            for j in range(len(book_deal)):
                book = Book.objects.get(id=book_deal[j].book_id)
                books[book] = book_deal[j].number
                totalPrice += int(book_deal[j].number) * float(book.price_old)
                storePrice += int(book_deal[j].number) * float(book.price_ori)
            tmpdeal_dict['totalPrice'] = totalPrice
            tmpdeal_dict['savePrice'] = storePrice - totalPrice 
            tmpdeal_dict['books'] = books
            deals[tmpdeal] = tmpdeal_dict
        if len(deals) > 0:
            dealkeys = deals.keys()
            dealkeys.reverse()
            return render_to_response("page/ordershow.jinja", {'deals':deals, \
                                                            'dealkeys':dealkeys}, RequestContext(request))
        else:
            return render_to_response("page/ordershow.jinja", {}, RequestContext(request))
    else:
        return render_to_response("page/ordershow.jinja", {}, RequestContext(request))

#卖书
def selling(request):
    form = SellForm(request.POST)
    dealid = int(time.strftime('%Y%m%d',time.localtime(time.time())) + '20001')
    try:
        maxid = int(Sell_Deal.objects.order_by('-id')[0].id)
        if maxid >= dealid:
            dealid = maxid + 1
    except Exception, e:
        print e
    emailtext = ''
    if form.is_valid():
        data = form.cleaned_data
        phone = data['sellformphone']
        address = data['sellformaddress']
        remark = data['sellformremark']
        sellDeal = Sell_Deal.objects.create(
                                           id=dealid,
                                           status=3,
                                           address=address,
                                           phone=phone,
                                           remark=remark,
                                           )
        sellDeal.status = 4
        sellDeal.save()
        emailtext += '订单号：' + str(dealid) + '\n'
        emailtext += '备注：' + remark + '\n'
        emailtext += '时间：' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '\n'
        emailtext += 'url：' + 'http://shumaimai.cn/admin-ext/order/sell/' + str(dealid) + '/edit/'
        send_mail('卖书，电话：' + str(phone) + '，地址：' + address + '，订单号：' + str(dealid), \
                emailtext, settings.DEFAULT_FROM_EMAIL, settings.DEFAULT_TO_EMAIL, )
        return render_to_response("page/index.jinja", {'page':'sell'}, RequestContext(request))
    else:
        return render_to_response("page/index.jinja", {'message':u'&nbsp;&nbsp;&nbsp;非法操作'}, RequestContext(request))

#卖书页面
#@cache_page
def sellshow(request):
    return render_to_response("page/sell.jinja", {}, RequestContext(request))

#代购页面
#@cache_page
def buybehalfshow(request):
    return render_to_response("page/buybehalf.jinja", {}, RequestContext(request))

#确认页面
@cache_page
def confirmshow(request):
    message = request.GET['message']
    page = request.GET['page']
    dealid = request.GET['dealid']
    score = request.GET['score']
    return render_to_response("page/confirm.jinja", {'message':message, 'page':page, \
                                                    'dealid':dealid, 'score':score}, RequestContext(request))
#提示页面
def alertshow(request):
    return render_to_response("page/alert.jinja", {}, RequestContext(request))

#取消订单
def cancelorder(request):
    deal_id = request.GET['dealid']
    user_id = request.session['_auth_user_id']
    deal = Deal.objects.filter(id=deal_id, user_id=user_id, status=3)
    if len(deal) > 0:
        user_profile = UserProfile.objects.get(user_id=user_id)
        user_profile.score += deal[0].score
        deal[0].status=5
        deal[0].finishTime = datetime.datetime.now()
        user_profile.save()
        deal[0].save()
        emailtext = ''
        emailtext += '取消订单：' + str(deal_id) 
        send_mail('取消订单：' + str(deal_id), emailtext, settings.DEFAULT_FROM_EMAIL, settings.DEFAULT_TO_EMAIL, )
        response = HttpResponse()
        result = json.dumps({'state':'1'})
        response.write(result)
        return response
    else:
        return render_to_response("page/index.jinja", {'message':u'&nbsp;&nbsp;&nbsp;非法操作'}, RequestContext(request))
