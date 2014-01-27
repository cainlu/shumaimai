#coding=utf-8

from django.http import *
from django.shortcuts import *
from django.contrib.auth import *
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import Group 
from django.core.urlresolvers import *
from django.conf import settings
from django.dispatch import *

from models import *
from forms import *
from utils import *

from main.utils import *

from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

def login(request):
    """ 
    return login page 
    handle login matters
    """
    refer = None
    try:
        refer = request.META['HTTP_REFERER']
    except:
        refer = reverse('index')
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            username = data['username']
            password = data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else: 
                return render_to_response('page/login.jinja', context_instance, RequestContext(request))
        else:
            context_instance['login_form'] = login_form
            return render_to_response('page/login.jinja', context_instance, RequestContext(request))
    else:
        context_instance['login_form'] = LoginForm(label_suffix='')
        return render_to_response('page/login.jinja', context_instance, RequestContext(request))

def logout(request):
    """
    return index
    handle logout matters
    """
    auth_logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    """
    return register page
    handle register matters
    """
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            cleaned_data = register_form.cleaned_data
            username = dict_get(cleaned_data, 'username')
            password = dict_get(cleaned_data, 'password')
            email = dict_get(cleaned_data, 'email')
            user = User.objects.create_user(username,email,password)
            profile = user.get_profile()
            email = dict_get(cleaned_data, 'email')
            if not email is None:
                user.email = email
            last_name = dict_get(cleaned_data, 'last_name')
            if not last_name is None:
                user.last_name = last_name
            first_name = dict_get(cleaned_data, 'first_name')
            if not first_name is None:
                user.first_name = first_name
            gender = dict_get(cleaned_data, 'gender')
            if not gender is None:
                profile.gender = gender
            address = dict_get(cleaned_data, 'address')
            if not address is None:
                profile.address = address
            phone = dict_get(cleaned_data, 'phone')
            if not phone is None:
                profile.phone = phone
            school = dict_get(cleaned_data, 'school')
            if not school is None:
                profile.school = school
            faculty = dict_get(cleaned_data, 'faculty')
            if not faculty is None:
                profile.faculty = faculty
            major = dict_get(cleaned_data, 'major')
            if not major is None:
                profile.major = major
            profile.score = 0
            user.save()
            profile.save()
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponseRedirect(reverse('index'))
        else:
            context_instance['register_form'] = register_form
            return render_to_response('page/register.jinja', context_instance, RequestContext(request))
    else:
        context_instance['register_form'] = RegisterForm(label_suffix='')
        return render_to_response('page/register.jinja', context_instance, RequestContext(request))

def user_center(request):
    """ return user center page """
    user = None
    if request.user.is_authenticated():
        return render_to_response('page/user_center.jinja', context_instance, RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('user_login'))

def user_profile(request):
    """ 
    return user profile edit page
    handle user profile edit matters
    """
    user = None
    if request.user.is_authenticated():
        user = request.user
        profile = user.get_profile()
        context_instance['password_change_form'] = PasswordChangeForm()
        if request.method == 'POST':
            user_form = UserForm(request.POST)
            context_instance['user_profile_note'] = u''
            if user_form.is_valid():
                cleaned_data = user_form.cleaned_data
                email = dict_get(cleaned_data, 'email')
                if not email is None:
                    user.email = email
                last_name = dict_get(cleaned_data, 'last_name')
                if not last_name is None:
                    user.last_name = last_name
                first_name = dict_get(cleaned_data, 'first_name')
                if not first_name is None:
                    user.first_name = first_name
                gender = dict_get(cleaned_data, 'gender')
                if not gender is None:
                    profile.gender = gender
                address = dict_get(cleaned_data, 'address')
                if not address is None:
                    profile.address = address
                phone = dict_get(cleaned_data, 'phone')
                if not phone is None:
                    profile.phone = phone
                school = dict_get(cleaned_data, 'school')
                if not school is None:
                    profile.school = school
                user.save()
                profile.save()
                context_instance['user_profile_note'] = u'个人信息修改成功'
            context_instance['user_form'] = user_form
            return render_to_response('page/user_profile.jinja', context_instance, RequestContext(request))
        else:
            data_user_form = {
                'email' : user.email,
                'last_name':user.last_name,
                'first_name':user.first_name,
                'gender':profile.gender,
                'address' : profile.address,
                'phone' : profile.phone,
                'school' : profile.school,
                'faculty':profile.faculty,
                'major':profile.major,
            }
            context_instance['user_form'] = UserForm(initial=data_user_form, label_suffix='')
            return render_to_response('page/user_profile.jinja', context_instance, RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('user_login'))

def user_password_change(request):
    user = None
    if request.user.is_authenticated():
        user = request.user
        profile = user.get_profile()
        if request.method == 'POST':
            password_change_form = PasswordChangeForm(request.POST)
            if password_change_form.is_valid():
                cleaned_data = password_change_form.cleaned_data
                password_old = dict_get(cleaned_data, 'password_old')
                password_new = dict_get(cleaned_data, 'password_new')
                if user.check_password(password_old):
                    user.set_password(password_new)
                    user.save()
                    context_instance["password_change_note"] = u"密码修改成功"
                else:
                    context_instance["password_change_note"] = u"原密码不正确"
            context_instance["password_change_form"] = password_change_form
        else:
            context_instance['password_change_form'] = PasswordChangeForm()
        data_user_form = {
            'email' : user.email,
            'last_name':user.last_name,
            'first_name':user.first_name,
            'gender':profile.gender,
            'address' : profile.address,
            'phone' : profile.phone,
            'school' : profile.school,
            'faculty':profile.faculty,
            'major':profile.major,
        }
        context_instance['user_form'] = UserForm(initial=data_user_form, label_suffix='')
        return render_to_response('page/user_profile.jinja', context_instance, RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('user_login'))

def confirm(request, confirmation_key):
    """ return register confirmation result page """
    confirmation_key = confirmation_key.lower()
    confirmation = EmailConfirmation.objects.confirm_email(confirmation_key)
    if confirmation:
        if confirmation.confirm_type == 1: 
            user = confirmation.user
            user.is_active = True
            user.save()
            return render_to_response("page/email_confirmed.jinja", {"confirmation": confirmation,}, RequestContext(request))
    return HttpResponse("Confirm error.")

def captcha_refresh(request):
    response = HttpResponse()
    new_captcha_key = CaptchaStore.generate_key()
    new_captcha_image = captcha_image_url(new_captcha_key)
    new_captcha_hashkey = new_captcha_image.split('/')[3]
    result = json.dumps({'state':'1', 'new_captcha_image':new_captcha_image, \
                         'new_captcha_hashkey':new_captcha_hashkey})
    response.write(result)
    return response


