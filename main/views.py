#coding=utf-8

import os
from django.http import *
from django.shortcuts import *

def index(request):
    return render_to_response(
            'page/index.jinja',
            {},
            RequestContext(request)
        ) 


def base_404(request):
    url = request.get_full_path()
    return HttpResponse('不好意思，您需要的页面没有没找到。如果是个必要的页面，希望您能联系我们，谢谢！')

def base_500(request):
    return HttpResponse('服务器出错了～～希望您能联系我们，谢谢！')


def footer_about_us(request):
    return render_to_response(
            'page/footer_about_us.jinja',
            {},
            RequestContext(request)
        ) 

def footer_contact_us(request):
    return render_to_response(
            'page/footer_contact_us.jinja',
            {},
            RequestContext(request)
        ) 

def footer_job(request):
    return render_to_response(
            'page/footer_job.jinja',
            {},
            RequestContext(request)
        ) 

def footer_sell(request):
    return render_to_response(
            'page/footer_sell.jinja',
            {},
            RequestContext(request)
        ) 


def footer_buy(request):
    return render_to_response(
            'page/footer_buy.jinja',
            {},
            RequestContext(request)
        ) 


def footer_return(request):
    return render_to_response(
            'page/footer_return.jinja',
            {},
            RequestContext(request)
        ) 


def footer_subscribe(request):
    return render_to_response(
            'page/footer_subscribe.jinja',
            {},
            RequestContext(request)
        ) 


def footer_quality(request):
    return render_to_response(
            'page/footer_quality.jinja',
            {},
            RequestContext(request)
        ) 
