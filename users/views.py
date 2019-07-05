import hashlib
from random import randint

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


# 注册
def register(request):
    form = UserRegisterForm
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            user = User.objects.create(username=username, password=hashlib.sha1(password.encode('utf8')).hexdigest(),
                                       email=email, phone=phone)
            user.save()
            return redirect(reverse('goods:index'))
    return render(request, 'goods/register.html', context={
            'form': form
        })


def person(request):
    return render(request, 'goods/my-user.html')


code = None


def sms(request, phone):
    if request.method == 'POST':
        num = randint(100000, 999999)
        request.session['smscode'] = str(num)
        sms(phone, {'code': str(num), **SMSCONFIG})
        return JsonResponse({'code': 1})


