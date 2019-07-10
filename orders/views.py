import json
import time
import uuid

from django.http import JsonResponse
from django.shortcuts import render


# Create your views here.
from django.views.decorators.csrf import csrf_exempt

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
            orderproduct.price = cart.unit_price
            orderproduct.product = cart.product
            orderproduct.order_info = orderinfo
            orderproduct.save()
            cart.delete()
        request.session.delete("cart_info_list")
        request.session["orderinfo_id"] = orderinfo.id
        return JsonResponse({'code': 0})
    orderinfo = OrderInfo.objects.get(pk=request.session["orderinfo_id"])
    order_product_list = orderinfo.orderproduct_set.all()
    return render(request, 'goods/d-success.html', context={"orderinfo": orderinfo, "order_product_list": order_product_list})


