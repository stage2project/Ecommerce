from collections import Counter

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import TbSpu, TbSku, TbSpuPics, TbSkuAttr


# Create your views here.
def index(request):
    return render(request, 'goods/index.html')


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
    return render(request, 'goods/details.html', context={'attr_dict': attr_dict, 'title': spu.title, 'price': price})


@csrf_exempt
def get_price(request, spu_id):
    if request.method == "POST" and request.is_ajax():
        skus = TbSpu.objects.get(unique_code=spu_id).skus.all()
        sku_id_list = [sku.id for sku in skus]
        attr_list = []
        for attr in request.POST:
            attr_list.append(TbSkuAttr.objects.filter(attr_key=attr, attr_value=request.POST.get(attr), sku_id__in=sku_id_list).values('sku_id'))
        res = []
        for i in range(len(attr_list)):
            for j in attr_list[i]:
                res.append(j.get('sku_id'))

        res = dict(Counter(res))

        sku_id = [key for key, value in res.items()if value == len(attr_list)][0]
        price = TbSku.objects.get(pk=sku_id).price
        return JsonResponse({'code': 0, 'msg': '成功', 'price': price})
    return redirect(reverse('goods:index'))
