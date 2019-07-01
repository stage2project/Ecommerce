from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from backmanage.models import *


# Create your views here.
from goods.models import TbCategory, TbAttributeKey


def add_competence(request):
    # comp = {'超级管理员':'拥有至高无上的权利,操作系统的所有权限','普通管理员':'拥有网站的系统大部分使用权限，没有权限管理功能'}
    # print(111111111)
    # for name,description in comp.items():
    #     res = Competence()
    #     res.name = name
    #     print(res.name)
    #     res.description = description
    #     print(res.description)
    #     res.save()
    return HttpResponse('添加权限')


def index(request):
    date = datetime.now()
    return render(request, 'backmanage/index.html',context={'date':date})


def login(request):
    return render(request, 'backmanage/login.html')


def account_detail(request):
    return render(request, 'backmanage/Account_Details.html')


def add_brand(request):
    return render(request, 'backmanage/Add_Brand.html')


def admin_competence(request):
    return render(request, 'backmanage/admin_Competence.html')


def admin_info(request):
    return render(request, 'backmanage/admin_info.html')


def administrator(request):
    return render(request, 'backmanage/administrator.html')


def ads_list(request):
    return render(request, 'backmanage/Ads_list.html')


def advertising(request):
    return render(request, 'backmanage/advertising.html')


def amount(request):
    return render(request, 'backmanage/Amounts.html')


def article_add(request):
    return render(request, 'backmanage/article_add.html')


def article_list(request):
    return render(request, 'backmanage/article_list.html')


def article_sort(request):
    return render(request, 'backmanage/article_Sort.html')


def brand_details(request):
    return render(request, 'backmanage/Brand_detailed.html')


def brand_manage(request):
    return render(request, 'backmanage/Brand_Manage.html')


def category_manage(request):
    category = TbCategory.objects.values('id', 'name', 'parentid').filter(status=0).order_by('order').all()
    return render(request, 'backmanage/Category_Manage.html', context={'categorys': category})


def category_list(request):
    category = TbCategory.objects.filter(status=0).order_by('order').all()
    count = TbCategory.objects.filter(status=0).count()
    all_big_category = TbCategory.objects.filter(status=0, parentid=0).all()
    # todo 按照大类目分组显示小类目
    return render(request, 'backmanage/Category_list.html', context={'categorys': category, 'count': count, 'all_big_category': all_big_category})


@csrf_exempt
def category_add(request):
    all_big_category = TbCategory.objects.filter(status=0, parentid=0).all()
    if request.method == "POST":
        category = TbCategory()
        name = request.POST['name']
        order = request.POST['order']
        parentid = request.POST['parentid']
        description = request.POST['description']
        category.name = name
        category.parentid = parentid
        category.description = description
        category.order = order
        category.save()
        # todo 增加小类目时，列表未更新
        return redirect(reverse('backmanage:category_list'))
    return render(request, 'backmanage/Category_add.html', context={'all_big_category': all_big_category})


@csrf_exempt
def category_update(request, cid=None):
    if request.method == 'POST':
        category = TbCategory.objects.get(pk=request.POST.get('cid'))
        name = request.POST.get('name')
        parentid = request.POST.get('parentid')
        description = request.POST.get('description')
        order = request.POST.get('order')
        category.name = name
        category.parentid = parentid
        category.description = description
        category.order = order
        category.save()
        # todo 修改所属分类时，列表未更新
        return redirect(reverse('backmanage:category_list'))
    category = TbCategory.objects.get(pk=cid)
    all_big_category = TbCategory.objects.filter(status=0, parentid=0).all()
    # TODO  cid不存在时错误页面没有
    if not category:
        return HttpResponse("板块不存在")
    return render(request, 'backmanage/Category_update.html', context={"category": category, 'all_big_category': all_big_category})


def competence(request):
    return render(request, 'backmanage/Competence.html')


def cover_management(request):
    return render(request, 'backmanage/Cover_management.html')


def feedback(request):
    return render(request, 'backmanage/Feedback.html')


def guestbook(request):
    return render(request, 'backmanage/Guestbook.html')


def home(request):
    date = datetime.now()
    ip = request.META['REMOTE_ADDR']
    return render(request, 'backmanage/home.html', context={'date':date,'ip':ip})


def integration(request):
    return render(request, 'backmanage/integration.html')


def member_grading(request):
    return render(request, 'backmanage/member-Grading.html')


def member_show(request):
    return render(request, 'backmanage/member-show.html')


def order_chart(request):
    return render(request, 'backmanage/Order_Chart.html')


def order_detailed(request):
    return render(request, 'backmanage/order_detailed.html')


def order_handling(request):
    return render(request, 'backmanage/Order_handling.html')


def orderform(request):
    return render(request, 'backmanage/Orderform.html')


def payment_configure(request):
    return render(request, 'backmanage/Payment_Configure.html')


def payment_detail(request):
    return render(request, 'backmanage/Payment_details.html')


def payment_method(request):
    return render(request, 'backmanage/payment_method.html')


def picture_add(request):
    return render(request, 'backmanage/picture-add.html')


def pruduct_list(request):
    return render(request, 'backmanage/Products_List.html')


def refund(request):
    return render(request, 'backmanage/Refund.html')


def refund_detailed(request):
    return render(request, 'backmanage/Refund_detailed.html')


def shop_list(request):
    return render(request, 'backmanage/Shop_list.html')


def shopping_detailed(request):
    return render(request, 'backmanage/shopping_detailed.html')


def shops_audit(request):
    return render(request, 'backmanage/Shops_Audit.html')


def sort_ads(request):
    return render(request, 'backmanage/Sort_ads.html')


def system_logs(request):
    return render(request, 'backmanage/System_Logs.html')


def system_section(request):
    return render(request, 'backmanage/System_section.html')


def systems(request):
    return render(request, 'backmanage/Systems.html')


def transaction(request):
    return render(request, 'backmanage/transaction.html')


def user_list(request):
    return render(request, 'backmanage/user_list.html')


def attribute_list(request, cid):
    print(cid)
    category = TbCategory.objects.get(pk=cid)
    attribute_key_all = category.attr_key.all()
    common_attribute = []
    special_attribute = []
    for key in attribute_key_all:
        if key.is_common:
            common_attribute.append({'id': key.id, "name": key.name, 'values': []})
        else:
            special_attribute.append({'id': key.id, "name": key.name, 'values': []})
    for key in common_attribute:
        attribute = TbAttributeKey.objects.get(pk=key['id'])
        attribute_values = attribute.attr_value.all()
        for value in attribute_values:
            key['values'].append({'id': value.id, 'value': value.value})
    for key in special_attribute:
        attribute = TbAttributeKey.objects.get(pk=key['id'])
        attribute_values = attribute.attr_value.all()
        for value in attribute_values:
            key['values'].append({'id': value.id, 'value': value.value})
    print(common_attribute, special_attribute)
    return render(request, 'backmanage/Attribute_list.html', context={'common_attribute': common_attribute, 'special_attribute': special_attribute})


def attribute_update(request):
    return None


def attribute_delete(request):
    return None


def attribute_add(request):
    return None