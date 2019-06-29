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
    print(skus[0].sku_attr.all())
    return render(request, 'goods/details.html')
