import json
import os
import time

from alipay import AliPay
from django.http import JsonResponse
from django.shortcuts import render


# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from Ecommerce.settings import BASE_DIR, MERCHANT_PRIVATE_KEY_PATH, ALIPAY_PUBLIC_KEY_PATH, APP_ID
from cart.models import CartInfo
from orders.models import OrderInfo, OrderProduct
from users.models import Address, User


@csrf_exempt
def confirm_order(request):
    cart_list = []
    total_amount = 0
    if request.method == "POST":
        cart_info_list = json.loads(request.POST.get('cart_info'))
        request.session["cart_info_list"] = cart_info_list
        return JsonResponse({'code': 0})
    if request.session.get("cart_info_list"):
        cart_info_list = request.session.get("cart_info_list")
        for cart_id in cart_info_list:
            total_amount += CartInfo.objects.get(pk=cart_id).total_price
            cart_list.append(CartInfo.objects.get(pk=cart_id))
    user = User.objects.get(pk=request.session.get('uid'))
    address_list = Address.objects.filter(user=user).order_by('is_default').all()
    return render(request, 'goods/confirm_order.html', context={'address_list': address_list, 'cart_list': cart_list, 'total_amount': total_amount})


@csrf_exempt
def commit_order(request):
    if request.method == "POST":
        address = Address.objects.get(pk=request.POST.get('address_id'))
        cart_info_list = request.session.get("cart_info_list")
        total_product_price = 0
        total_product_count = 0
        for cart_id in cart_info_list:
            total_product_price += CartInfo.objects.get(pk=cart_id).total_price
            total_product_count += CartInfo.objects.get(pk=cart_id).product_count
        orderinfo = OrderInfo()
        orderinfo.order_id = int(time.time())
        orderinfo.product_count = total_product_count
        orderinfo.product_price = total_product_price
        orderinfo.user = User.objects.get(pk=request.session.get('uid'))
        orderinfo.addr = address
        orderinfo.save()
        for cart_id in cart_info_list:
            cart = CartInfo.objects.get(pk=cart_id)
            orderproduct = OrderProduct()
            orderproduct.count = cart.product_count
            orderproduct.price = cart.unit_price * orderproduct.count
            orderproduct.product = cart.product
            orderproduct.order_info = orderinfo
            orderproduct.save()
            cart.delete()
        request.session.pop("cart_info_list")
        request.session["orderinfo_id"] = orderinfo.id
        return JsonResponse({'code': 0})
    orderinfo = OrderInfo.objects.get(pk=request.session["orderinfo_id"])
    order_product_list = orderinfo.orderproduct_set.all()
    return render(request, 'goods/d-success.html', context={"orderinfo": orderinfo, "order_product_list": order_product_list})


def pay_order(request):
    alipay = AliPay(
        appid=APP_ID,
        app_notify_url=None,
        app_private_key_path=MERCHANT_PRIVATE_KEY_PATH,
        alipay_public_key_path=ALIPAY_PUBLIC_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        debug=True,  # 默认False,
    )
    if request.is_ajax() and request.META.get('HTTP_REFERER').split('/')[-2] == "order_manage":
        order = OrderInfo.objects.get(order_id=request.GET.get('order_id'))
    else:
        order = OrderInfo.objects.get(pk=request.session["orderinfo_id"])
    subject = "SX商城支付订单-%s" % order.order_id
    total_pay = order.product_price

    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order.order_id,
        total_amount=str(total_pay),
        subject=subject,
        return_url=None,
        notify_url=None  # 可选, 不填则使用默认notify url
    )

    pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
    if not request.is_ajax():
        request.session.pop("orderinfo_id")
    return JsonResponse({"res": 3, "pay_url": pay_url})


def check_pay_status(request):
    user = User.objects.get(pk=request.session.get('uid'))
    order_list = OrderInfo.objects.filter(user=user).all()
    for order in order_list:
        alipay = AliPay(
            appid=APP_ID,
            app_notify_url=None,
            app_private_key_path=MERCHANT_PRIVATE_KEY_PATH,
            alipay_public_key_path=ALIPAY_PUBLIC_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
            debug=True,  # 默认False,
        )
        response = alipay.api_alipay_trade_query(
            out_trade_no=order.order_id
        )
        print(response)
        if response.get('trade_status') == "TRADE_SUCCESS":
            order.order_status = 2
            order.pay_date = response.get("send_pay_date")
            order.trance_num = response['trade_no']
            order.save()
    return order_list

