from collections import Counter
from copy import deepcopy

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from backmanage.models import Advertisement
from cart.models import CartInfo
from users.models import User
from .models import TbSpu, TbSku, TbSpuPics, TbSkuAttr, TbCategory, TbBrand


# Create your views here.
def index(request):
    all_big_category = TbCategory.objects.filter(status=0, parentid=0).all()
    all_small_category = TbCategory.objects.filter(~Q(parentid=0) & Q(status=0)).all()
    all_brand = TbBrand.objects.filter(yn=0).all()
    carousel_advertisement = Advertisement.objects.filter(yn=0, type=0).order_by('order', '-create_time').all()
    static_advertisement = Advertisement.objects.filter(yn=0, type=1).order_by('order', '-create_time').all()[:4]
    banner_advertisement = Advertisement.objects.filter(yn=0, type=2).order_by('order', '-create_time').all()[:1]
    all_spu = TbSpu.objects.all()
    spu_pic_list = []
    for spu in all_spu:
        spu_pic_list.append({"spu": spu, "spu_pic": spu.spu_pic.first()})
    all_pics = TbSpuPics.objects.all()
    if request.session.get('uid'):
        amount = CartInfo.objects.filter(user=User.objects.get(pk=request.session.get('uid'))).count()
    else:
        amount = 0
    return render(request, 'goods/index.html', context={"all_big_category": all_big_category, "all_small_category": all_small_category,
                                                        "all_brand": all_brand, 'carousel_advertisement': carousel_advertisement,
                                                        'static_advertisement': static_advertisement, "banner_advertisement": banner_advertisement,
                                                        'spu_pic_list': spu_pic_list, 'amount': amount})


def details(request, spu_id):
    spu = TbSpu.objects.get(pk=spu_id)
    skus = spu.skus.all()
    sku_default = skus.first()
    attr_obj_list = []
    for sku in skus:
        for attr in sku.sku_attr.all():
            attr_obj_list.append(attr)
    attr_dict = {}
    for attr_obj in attr_obj_list:
            attr_dict[attr_obj.attr_key.name+"_"+str(attr_obj.attr_key.id)] = []

    for attr_obj in attr_obj_list:
            attr_dict[attr_obj.attr_key.name+"_"+str(attr_obj.attr_key.id)].append(attr_obj.attr_value.value+"_"+str(attr_obj.attr_value.id))

    def get_split_1(str):
        return str.split('_')[1]
    for key in attr_dict:
        value_list = list(set(attr_dict[key]))
        value_list.sort(key=get_split_1)
        attr_dict[key] = value_list

    price = sku_default.price
    if request.session.get('uid'):
        amount = CartInfo.objects.filter(user=User.objects.get(pk=request.session.get('uid'))).count()
    else:
        amount = 0
    pic_default = spu.spu_pic.order_by('id').first()
    pic_list = spu.spu_pic.order_by('id').all()
    return render(request, 'goods/details.html', context={'attr_dict': attr_dict, 'title': sku_default.title, 'price': price, 'amount': amount, 'sku_id': sku_default.id, 'spu': spu , 'pic_default': pic_default, "pic_list": pic_list})


@csrf_exempt
def get_price(request, spu_id):
    if request.method == "POST" and request.is_ajax():
        print(request.POST)
        skus = TbSpu.objects.get(unique_code=spu_id).skus.all()
        sku_id_list = [sku.id for sku in skus]
        attr_list = []
        for attr in request.POST:
            attr_list.append(TbSkuAttr.objects.filter(attr_key=attr, attr_value=request.POST.get(attr), sku_id__in=sku_id_list).values('sku_id'))
        print(attr_list)
        res = []
        for i in range(len(attr_list)):
            for j in attr_list[i]:
                res.append(j.get('sku_id'))
        print(res)
        res = dict(Counter(res))
        print(res)
        sku_id = [key for key, value in res.items()if value == len(attr_list)][0]
        price = TbSku.objects.get(pk=sku_id).price
        title = TbSku.objects.get(pk=sku_id).title
        return JsonResponse({'code': 0, 'msg': '成功', 'price': price, 'sku_id': sku_id, 'title': title})
    return redirect(reverse('goods:index'))


def list_page(request, cid):
    all_big_category = TbCategory.objects.filter(status=0, parentid=0).all()
    all_small_category = TbCategory.objects.filter(~Q(parentid=0) & Q(status=0)).all()
    category = TbCategory.objects.get(pk=cid)
    all_brand = category.brand.all()
    all_spu = category.spus.all()
    spu_pic_list = []
    for spu in all_spu:
        spu_pic_list.append({"spu": spu, "spu_pic": spu.spu_pic.first()})
    attr_dict = {}
    all_attr_key = category.attr_key.all()
    for attr_key in all_attr_key:
        attr_dict[attr_key.name] = attr_key.attr_value.all()
    if request.session.get('uid'):
        amount = CartInfo.objects.filter(user=User.objects.get(pk=request.session.get('uid'))).count()
    else:
        amount = 0
    return render(request, 'goods/all-class.html', context={'all_brand': all_brand, "all_big_category": all_big_category,
                                                            "all_small_category": all_small_category, "attr_dict": attr_dict,
                                                            "spu_pic_list": spu_pic_list, "category": category, 'amount': amount})


@csrf_exempt
def spu_filter(request, cid):
    if request.method == "POST" and request.is_ajax():
        param = deepcopy(request.POST)
        if 'brand' in param:
            spus = TbCategory.objects.get(pk=cid).spus.filter(brand=TbBrand.objects.get(pk=param['brand'])).all()
            del param['brand']
        else:
            spus = TbCategory.objects.get(pk=cid).spus.all()
        if not param:
            res_spu_list = []
            for spu in spus:
                res_spu_list.append({'unique_code': spu.unique_code, 'spu_title': spu.title, 'list_price': spu.list_pirce, 'spu_pic': spu.spu_pic.all().first().pic})
            return JsonResponse({'code': 0, 'msg': '成功', 'spu_list': res_spu_list})
        sku_id_list = []
        for spu in spus:
            for sku in spu.skus.all():
                sku_id_list.append(sku.id)
        attr_list = []
        for attr in param:
            attr_list.append(TbSkuAttr.objects.filter(attr_key=attr, attr_value=param.get(attr),
                                                      sku_id__in=sku_id_list).values('sku_id'))
        res = []
        for i in range(len(attr_list)):
            for j in attr_list[i]:
                res.append(j.get('sku_id'))
        res = dict(Counter(res))
        sku_id_list = [key for key, value in res.items() if value == len(attr_list)]
        spu_list = []
        for sku_id in sku_id_list:
            spu_list.append(TbSku.objects.get(pk=sku_id).spu)
        spu_list = list(set(spu_list))
        res_spu_list = []
        for spu in spu_list:
            res_spu_list.append({'unique_code': spu.unique_code, 'spu_title': spu.title, 'list_price': spu.list_pirce, 'spu_pic': spu.spu_pic.all().first().pic})

        return JsonResponse({'code': 0, 'msg': '成功', 'spu_list': res_spu_list})


def cart_manage(request):
    user = User.objects.get(pk=request.session.get('uid'))
    cart_list = CartInfo.objects.filter(user=user).all()
    total_price = 0
    for cart in cart_list:
        total_price += cart.total_price
    return render(request, 'goods/my-Cart.html', context={'cart_list': cart_list, 'total_price': total_price})


@csrf_exempt
def add_cart(request):
    sku = TbSku.objects.get(pk=request.POST.get('sku_id'))
    user = User.objects.get(pk=request.session.get('uid'))
    cart = CartInfo.objects.filter(product=sku, user=user).first()
    if cart:
        cart.product_count += int(request.POST.get('product_number'))
        cart.total_price = cart.product_count * cart.unit_price
    else:
        cart = CartInfo()
        cart.user = user
        cart.product = sku
        cart.product_count = int(request.POST.get('product_number'))
        cart.unit_price = TbSku.objects.get(pk=request.POST.get('sku_id')).price
        cart.total_price = cart.unit_price * cart.product_count
    cart.save()
    amount = CartInfo.objects.filter(user=user).count()
    return JsonResponse({'code': 0, 'msg': 'success', 'amount': amount})


def update_cart(request):
    cart = CartInfo.objects.get(pk=request.GET.get('id'))
    cart.product_count = request.GET.get('num')
    cart.total_price = cart.unit_price * int(request.GET.get('num'))
    cart.save()
    return JsonResponse({'code': 0, 'msg': 'success'})


def del_cart_item(request):
    cart = CartInfo.objects.get(pk=request.GET.get('id'))
    cart.delete()
    return JsonResponse({'code': 0, 'msg': 'success'})


@csrf_exempt
def buy_now(request):
    sku = TbSku.objects.get(pk=request.POST.get('sku_id'))
    if sku.cartinfo_set.exists():
        cart = sku.cartinfo_set.all()[0]
        cart.delete()
    user = User.objects.get(pk=request.session.get('uid'))
    cart = CartInfo()
    cart.user = user
    cart.product = sku
    cart.product_count = int(request.POST.get('product_number'))
    cart.unit_price = TbSku.objects.get(pk=request.POST.get('sku_id')).price
    cart.total_price = cart.unit_price * cart.product_count
    cart.save()
    request.session["cart_info_list"] = [cart.id]
    return JsonResponse({'code': 0, 'msg': 'success'})
