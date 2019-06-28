import json
import collections

from django.shortcuts import render
from .models import TbSpu, TbSku, TbSkuPics


# Create your views here.
def index(request):
    return render(request, 'goods/index.html')


def details(request, spu_id):
    spu = TbSpu.objects.get(pk=spu_id)
    print(spu.title)
    skus = spu.skus.all()
    print(skus)
    attr = {}
    for i in skus:
        attr_dict = json.loads(i.attr_json)
        print(attr_dict)
        for key in attr_dict:
            attr[key] = []
    for i in skus:
        attr_dict = json.loads(i.attr_json)
        print(attr_dict)
        for key in attr_dict:
            attr[key].append(attr_dict[key])
    {'颜色': {'value': 1, 'context': [{"红色": 1}, {"金色": 2}]}}
    print(attr)

    return render(request, 'goods/details.html')
