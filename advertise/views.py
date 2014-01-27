#coding=utf-8

from django.http import *
from django.shortcuts import *
from django.conf import settings
from advertise.models import *
from book.models import *
from django.contrib.auth.models import *
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import json

recommend_list = ['9787040108200', '9787040119923', '9787040108217', '9787040116861', '9787040205497',
                  '9787040212778', '9787501171668', '9787560845685', '9787560835853', '9787040119916',
                  '9787802211216', '9787560823829', '9787560824222', '9787111289098', '9787560825540',
                  '9787560837284', '9787040212181', '9787040215076', '9787302055341', '9787302065074',
                  '9787040377460', '9787560843506', '9787544631358', '9787544631365']
#时间计算
def timecal():
    import datetime
    import time
    now = time.time()
    date1 = datetime.datetime.strptime('2013-04-10 20:00:00', '%Y-%m-%d %H:%M:%S')
    date2 = datetime.datetime.strptime('2013-04-11 00:00:00', '%Y-%m-%d %H:%M:%S')
    date1 = time.mktime(date1.timetuple())
    date2 = time.mktime(date2.timetuple())
    if now >= date1 and now <= date2:
        return 0
    elif now < date1:
        return (date1 - now) * 1000
    elif now > date2:
        return -1

#广告展示
def advertiseshow(request):
    all = request.GET.get('all')
    activity = request.GET.get('activity')
    comments = Ad_Comment.objects.filter(activity=activity).order_by('-time')
    comments = comments[:20]
    if activity == '1':
        advertises = Ad_Text.objects.filter(activity=activity).order_by('-time')
        advertises = advertises[:5]
        topFive = []
        topFive.append(Ad_Text.objects.get(id=29))
        topFive.append(Ad_Text.objects.get(id=17))
        topFive.append(Ad_Text.objects.get(id=20))
        topFive.append(Ad_Text.objects.get(id=25))
        topFive.append(Ad_Text.objects.get(id=28))
        return render_to_response("page/learning.jinja", {'advertises':advertises, \
                        'topFive':topFive, 'comments':comments, 'activity':activity,}, RequestContext(request))
    elif activity == '2':
        reading_time = timecal()
        advertises = Ad_Text.objects.filter(activity=activity).order_by('?')
        topFive = Ad_Text.objects.filter(activity=activity, type=1).order_by('-agree', '-time')[:5]
        topFive2 = Ad_Text.objects.filter(activity=activity, type=2).order_by('-agree', '-time')[:5]
        for advertise in advertises:
            advertise.context = advertise.context[:300]
        if not all:
            advertises = advertises[:8]
        return render_to_response("page/reading.jinja", {'advertises':advertises, \
                                    'topFive':topFive, 'topFive2':topFive2, 'comments':comments, \
                                    'activity':activity,'reading_time':reading_time,}, RequestContext(request))

#赞成
def advertiseagree(request):
    response = HttpResponse()
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    advertiseId = request.GET['id']
    advertise = Ad_Text.objects.get(id=advertiseId)
    activity = str(advertise.activity)
    ip_record = Ip_Record.objects.filter(ip=ip, action=1, object=advertiseId, activity=activity)
    if len(ip_record) > 0:
        result = json.dumps({'state':'2'})
    else:
        advertise.agree += 1
        advertise.save()
        ip_record = Ip_Record.objects.create(
            ip=ip,
            action=1,
            object=advertiseId,
            activity=activity,
            )
        ip_record.save()
        if activity == '1':
            result = json.dumps({'state':'1', 'text':'赞美他[' + str(advertise.agree) + ']'})
        elif activity == '2':
            result = json.dumps({'state':'1', 'text':'赞一下[' + str(advertise.agree) + ']'})
    response.write(result)
    return response

#反对
def advertisedisagree(request):
    response = HttpResponse()
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    advertiseId = request.GET['id']
    advertise = Ad_Text.objects.get(id=advertiseId)
    activity = str(advertise.activity)
    ip_record = Ip_Record.objects.filter(ip=ip, action=2, object=advertiseId, activity=activity)
    if len(ip_record) > 0:
        result = json.dumps({'state':'2'})
    else:
        advertise.disagree += 1
        advertise.save()
        ip_record = Ip_Record.objects.create(
            ip=ip,
            action=2,
            object=advertiseId,
            activity=activity,
            )
        ip_record.save()
        if activity == '1':
            result = json.dumps({'state':'1', 'text':'学习他[' + str(advertise.disagree) + ']'})
        elif activity == '2':
            result = json.dumps({'state':'1', 'text':'打酱油[' + str(advertise.disagree) + ']'})
    response.write(result)
    return response

#评论展示
def commentshow(request):
    reading_time = timecal()
    all = request.GET.get('all')
    advertiseid = request.GET['advertiseid']
    advertise = Ad_Text.objects.get(id=advertiseid)
    activity = str(advertise.activity)
    comments = Ad_Comment.objects.filter(object=advertiseid).order_by('-time')
    if not all:
        comments = comments[:20]
    right_five = Ad_Text.objects.filter(activity=activity).order_by('?')[0:5]
    if activity == '1':
        return render_to_response("page/learning_comment.jinja", {'advertise':advertise, 'comments':comments, \
                                    'commentshow': '1', 'right_five': right_five,}, RequestContext(request))
    elif activity == '2':
        return render_to_response("page/reading_comment.jinja", {'advertise':advertise, 'comments':comments, \
                                'commentshow': '1', 'right_five': right_five, 'reading_time':reading_time, \
                                }, RequestContext(request))
#留言板
def messageboard(request):
    response = HttpResponse()
    activity = request.POST['activity']
    objectid = request.POST['objectid']
    context = request.POST['context']
    if '_auth_user_id' in request.session:
        user_id = request.session['_auth_user_id']
        user = User.objects.filter(id=user_id)
        if len(user) > 0:
            author = user[0].username
    else:
        author = '海大学生'
    time = datetime.datetime.now()
    if int(objectid) > 0:
        object = Ad_Text.objects.get(id=objectid)
        text = '<div>' + author + '&nbsp;&nbsp;&nbsp;评论&nbsp;&nbsp;&nbsp;' + \
        '<a href="/advertise/commentshow/?advertiseid=' + str(object.id) + '">' + object.title + \
        '</a></div><div>' + str(time)[:19]+ '</div><div>' + context + '</div><br>'
        author += '||' + str(object.id) + '||' + object.title
    else:
        text = '<div>' + author + '</div><div>' + str(time)[:19]+ '</div><div>' + context + '</div><br>'
    Ad_Comment.objects.create(
        object=objectid,
        author=author,
        context=context,
        agree=0,
        disagree=0,
        time=time,
        activity=activity,
        )
    result = json.dumps({'state':'1', 'text':text})
    response.write(result)
    return response

def moreadvertise(request):
    response = HttpResponse()
    activity = request.GET['activity']
    page = int(request.GET['page'])
    advertises = Ad_Text.objects.filter(activity=activity).order_by('-time')
    totalnum = len(advertises)
    advertises = advertises[5 * page : 5 * (page + 1)]
    text = ''
    if activity == '1':
        for advertise in advertises:
            text += '''
            <tr>
                <td class='td_leftdown' rowspan=3>
                    <img src="/static/image/ad''' + str(advertise.id) + '''.jpg" class='ad_left_img'>
                </td>
                <td colspan=3>
                    <a href='/advertise/commentshow/?advertiseid=''' + str(advertise.id) + ''''>
                        ''' + str(advertise.title) + '''
                    </a>
                </td>
            </tr>
            <tr>
                <td class='author'>
                    ''' + str(advertise.author) + '''
                </td>
                <td colspan=2 class='td_leftmiddle2'>
                    <div class='div_leftmiddle'>
                        <a onclick='ajaxAgree(''' + str(advertise.id) + ''')' class='agreeA agree''' + str(advertise.id) + ''''>
                            赞美他[''' + str(advertise.agree) + ''']</a>
                        <a onclick='ajaxDisagree(''' + str(advertise.id) + ''')' class='disagreeA disagree''' + str(advertise.id) + ''''>
                            学习他[''' + str(advertise.disagree) + ''']</a>
                    </div>
                </td>
            </tr>
            <tr>
                <td colspan=3 class='td_leftmiddle'><div class='td_leftdown2'>''' + str(advertise.context) + '''</div></td>
            </tr>
            <tr height='20px'/>
            '''
        if totalnum >= 5 * (page + 1):
            text += '''<tr id='more''' + str(page + 1) + '''' onclick='ajaxMore("''' + activity + '''", "''' + str(page + 1) + '''")'><td colspan=4><input type="button" value="查看更多" class='morebutton'></td></tr>'''
        if page == 1:
            text += '''<tr id='blank''' + str(page + 1) + '''' height='1000px'/>'''
    result = json.dumps({'state':'1', 'text':text})
    response.write(result)
    return response

def morecomment(request):
    response = HttpResponse()
    activity = request.GET['activity']
    page = int(request.GET['page'])
    comments = Ad_Comment.objects.filter(activity=activity).order_by('-time')
    totalnum = len(comments)
    comments = comments[10 * page : 10 * (page + 1)]
    text = ''
    if avtivity == '1':
        for comment in comments:
            text += '''
            '''
        if totalnum >= 5 * (page + 1):
            text += ''''''
    result = json.dumps({'state':'1', 'text':text})
    response.write(result)
    return response

def welcome_new(request):
    new_books = Book.objects.filter(isbn__in=recommend_list).order_by('?')[:7]
    return render_to_response('page/welcome_new.jinja', {'new_books':new_books},  RequestContext(request))

