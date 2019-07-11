import hashlib
from random import randint

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.vendored.requests import auth
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from Ecommerce.settings import SMSCONFIG
from orders.models import OrderProduct, OrderInfo
from orders.views import check_pay_status
from users.models import User, Address
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
            sms = request.POST.get('sms')
            if sms == request.session['sms']:
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                email = form.cleaned_data.get('email')
                phone = form.cleaned_data.get('phone')
                user = User.objects.create(username=username, password=hashlib.sha1(password.encode('utf8')).hexdigest(),
                                           email=email, phone=phone)
                user.save()
                return redirect(reverse('users:login'))
            else:
                form.sms.error_messages = "验证码错误"

    return render(request, 'goods/register.html', context={
            'form': form
        })


def person(request):
    return render(request, 'goods/my-user.html')


def send_sms_tool(phone, templateParam, **kwargs):
    client = AcsClient(kwargs['ACCESS_KEY_ID'], kwargs['ACCESS_KEY_SECRET'], 'default')
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')
    request.add_query_param('PhoneNumbers', phone)
    request.add_query_param('SignName', kwargs['SignName'])
    request.add_query_param('TemplateCode', kwargs['TemplateCode'])
    request.add_query_param('TemplateParam', templateParam)
    client.do_action_with_exception(request)


def send_sms(request):
    print(request.GET.get('phone'))
    phone = request.GET.get('phone')
    if not phone:
        return JsonResponse({"code": 1, "msg": "phone number can not be null"})
    num = randint(100000, 999999)
    request.session['sms'] = str(num)
    send_sms_tool(phone, {'code': str(num)}, **SMSCONFIG)
    return JsonResponse({"code": 0, "msg": "succsss"})


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


def address_manage(request):
    user = User.objects.get(pk=request.session.get('uid'))
    address_list = Address.objects.filter(user=user).order_by('-is_default').all()
    count = Address.objects.filter(user=user).count()
    return render(request, 'goods/my-add.html', context={'address_list': address_list, 'count': count})


def evaluation_manage(request):
    return render(request, 'goods/my-p.html')


def order_manage(request):
    order_list = check_pay_status(request)
    order_product_list = OrderProduct.objects.all()
    return render(request, 'goods/my-d.html', context={'order_list': order_list, "order_product_list": order_product_list})


def collection_manage(request):
    return render(request, 'goods/my-s.html')


def order_info(request, order_id):
    order = OrderInfo.objects.get(order_id=order_id)
    order_product_list = order.orderproduct_set.all()
    return render(request, 'goods/my-d-info.html', context={'order': order, 'order_product_list': order_product_list})


def logout(request):
    request.session.pop("uid")
    request.session.pop("username")
    return redirect(reverse('goods:index'))


@csrf_exempt
def add_address(request):
    user = User.objects.get(pk=request.session.get('uid'))
    if Address.objects.filter(user=user).count() > 20:
        return JsonResponse({'code': 1, 'msg': '只能添加20个地址'})
    if not request.POST.get('a_email') or not request.POST.get('a_phone') or not request.POST.get('a_region') or not request.POST.get('a_place') or not request.POST.get('a_name') or not request.POST.get('fixed_telephone'):
        return JsonResponse({'code': 1, 'msg': '参数错误'})
    address = Address()
    address.a_email = request.POST.get('a_email')
    address.a_phone = request.POST.get('a_phone')
    address.a_region = request.POST.get('a_region')
    address.a_place = request.POST.get('a_place')
    address.a_name = request.POST.get('a_name')
    address.fixed_telephone = request.POST.get('fixed_telephone')
    address.user = user
    if Address.objects.filter(user=user).count() == 0:
        address.is_default = True
    address.save()
    return JsonResponse({'code': 0})


def set_default_address(request, address_id):
    user = User.objects.get(pk=request.session.get('uid'))
    old_default_address = Address.objects.filter(user=user, is_default=True).first()
    old_default_address.is_default = False
    old_default_address.save()
    address = Address.objects.get(pk=address_id)
    address.is_default = True
    address.save()
    return redirect(reverse('users:address_manage'))


@csrf_exempt
def edit_address(request):
    address = Address.objects.get(pk=request.POST.get('address_id'))
    address.a_email = request.POST.get('a_email')
    address.a_phone = request.POST.get('a_phone')
    address.a_region = request.POST.get('a_region')
    address.a_place = request.POST.get('a_place')
    address.a_name = request.POST.get('a_name')
    address.fixed_telephone = request.POST.get('fixed_telephone')
    address.save()
    return JsonResponse({'code': 0})


def del_address(request, address_id):
    address = Address.objects.get(pk=address_id)
    address.delete()
    return redirect(reverse('users:address_manage'))