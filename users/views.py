import hashlib
from random import randint

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.vendored.requests import auth
from django.shortcuts import render, redirect
from django.urls import reverse

from Ecommerce.settings import SMSCONFIG
from users.models import User
from users.forms import UserRegisterForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse


# Create your views here.


# 登录
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        send_flag = int(request.POST.get('type'))
        password = hashlib.sha1(password.encode('utf8')).hexdigest()
        # 0- 邮箱 1- 用户名， 2- 手机号
        if send_flag == 0:
            res1 = User.objects.filter(email=username, password=password)
            if len(res1) > 0:
                request.session['uid'] = res1[0].id
                request.session['username'] = res1[0].username
                return redirect(reverse('goods:index'))

        elif send_flag == 1:
            res2 = User.objects.filter(username=username, password=password)
            if len(res2) > 0:
                request.session['uid'] = res2[0].id
                request.session['username'] = res2[0].username
                return redirect(reverse('goods:index'))

        elif send_flag == 2:
            res3 = User.objects.filter(phone=username, password=password)
            if len(res3) > 0:
                request.session['uid'] = res3[0].id
                request.session['username'] = res3[0].username
                return redirect(reverse('goods:index'))
        else:
            return render(request, 'goods/login.html')
    return render(request, 'goods/login.html')


# 注册--form表单
def register(request):
    form = UserRegisterForm
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # sms = request.POST.get('sms')
            # if sms == request.session['sms']:
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            user = User.objects.create(username=username, password=hashlib.sha1(password.encode('utf8')).hexdigest(),
                                       email=email, phone=phone)
            user.save()
            return redirect(reverse('users:login'))

    return render(request, 'goods/register.html', context={
            'form': form
        })


def person(request):
    return render(request, 'goods/my-user.html')


# def send_sms(request, phone, templateParam, **kwargs):
#     client = AcsClient(kwargs['ACCESS_KEY_ID'], kwargs['ACCESS_KEY_SECRET'], 'default')
#     request = CommonRequest()
#     request.set_accept_format('json')
#     request.set_domain('dysmsapi.aliyuncs.com')
#     request.set_method('POST')
#     request.set_protocol_type('https')  # https | http
#     request.set_version('2017-05-25')
#     request.set_action_name('SendSms')
#     request.add_query_param('PhoneNumbers', phone)
#     request.add_query_param('SignName', kwargs['SignName'])
#     request.add_query_param('TemplateCode', kwargs['TemplateCode'])
#     request.add_query_param('TemplateParam', templateParam)
#     response = client.do_action_with_exception(request)
#     print(str(response, encoding='utf-8'))
#
#     if request.method == 'POST':
#         num = randint(100000, 999999)
#         request.session['sms'] = str(num)
#         send_sms(phone, {'code': str(num), **SMSCONFIG})
#         return JsonResponse({'code': 1})
#
def order(request):
    return render(request, 'goods/my-d.html')


def collect(request):
    return render(request, 'goods/my-s.html')


def sale(request):
    return render(request, 'goods/sale.html')


def retreat(request):
    return render(request, 'goods/retreat-cha.html')


def evaluation(request):
    return render(request, 'goods/my-p.html')


def address(request):
    return render(request, 'goods/my-add.html')


def address_manage(request):
    return render(request, 'goods/my-add.html')


def evaluation_manage(request):
    return render(request, 'goods/my-p.html')


def order_manage(request):
    return render(request, 'goods/my-d.html')


def collection_manage(request):
    return render(request, 'goods/my-s.html')


def order_info(request):
    return render(request, 'goods/my-d-info.html')


def logout(request):
    request.session.flush()
    return redirect(reverse('goods:index'))


def send_sms(request):
    return None