import hashlib
import json
import os
from datetime import datetime
from itertools import count
from random import randint

from django.contrib.messages.storage import session
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from Ecommerce import settings
from Ecommerce.settings import SECRET_KEY
from backmanage.models import *

import json

# Create your views here.
from backmanage.verfiCode import VerfiCode
from goods.models import TbCategory, TbAttributeKey, TbSpuPics
from goods.models import TbCategory, TbAttributeKey, TbAttributeValue
from goods.models import TbCategory, TbAttributeKey, TbAttributeValue, TbSku, TbBrand, TbSpu, TbSkuAttr
from users.models import User


def add_competence(request):
    comp = {'超级管理员': '拥有至高无上的权利,操作系统的所有权限', '普通管理员': '拥有网站系统大部分使用权限,无权限管理功能', '编辑管理员': '拥有部分权限,主要进行编辑功能,无编辑订单功能,权限分配功能'}
    for key, value in comp.items():
        res = Privilege()
        res.privilege_name = key
        res.describe = value
        res.menu_list = [0]
        res.save()
    return HttpResponse('添加权限')


def add_admin(request):
    admin = Admin()
    admin.admin_name = 'lixiaoni'
    admin.admin_password = hashlib.sha1(b'a123').hexdigest()
    admin.admin_age = '22'
    admin.admin_sex = False
    admin.admin_reg_date = datetime.now()
    admin.admin_login_ip = request.META['REMOTE_ADDR']
    admin.admin_login_addr = '北京海淀'
    admin.admin_email = '1134492261@qq.com'
    admin.admin_phone = 17635144631
    admin.admin_qq = '1134492261'
    admin.privilege = Privilege.objects.get(id=13)
    admin.save()
    return HttpResponse('add_admin')


def index(request):
    if request.session.get("admin_id"):
        username = request.session.get('admin_username')
        data = Privilege.objects.filter(admin=request.session.get("admin_id")).all()[0]
        return render(request, 'backmanage/index.html', context={'username': username, 'data': data})
    return redirect(reverse("backmanage:login"))


def login(request):
    if request.is_ajax():
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_hash = hashlib.sha1(password.encode('utf8')).hexdigest()
        code = request.POST.get('code')
        verficode = request.session['admin_verficode']
        res = Admin.objects.filter(admin_name=username, admin_password=password_hash).values('id', 'admin_name')
        if len(res) > 0 and verficode == code:  # 登录成功
            request.session['admin_id'] = res[0]['id']
            request.session['admin_username'] = res[0]['admin_name']
            return JsonResponse({'code': 1, 'msg': 'ok'}, safe=False)
        return JsonResponse({'code': 0, 'msg': 'failed'}, safe=False)
    return render(request, 'backmanage/login.html')


def account_detail(request):
    return render(request, 'backmanage/Account_Details.html')


def add_brand(request):
    all_big_category = TbCategory.objects.filter(status=0, parentid=0).all()
    all_small_category = TbCategory.objects.filter(status=0).exclude(parentid=0).all()
    if request.method == "POST":
        brand = TbBrand()
        brand.name = request.POST['bname']
        file = request.FILES.get('brlogo')
        try:
            path = os.path.join(settings.STATIC_ROOT, file.name)
        except Exception as e:
            path = os.path.join(settings.MEDIA_ROOT, file.name)
        ext = os.path.splitext(file.name)
        if len(ext) < 1 or not ext[1] in settings.ALLOWED_FILEEXTS:
            return redirect(reverse('backmanage:add_brand'))
        brand.logo = 'upload/' + file.name
        if os.path.exists(path):
            dir1 = datetime.today().strftime("%Y/%m/%d")
            dir = os.path.join(settings.MEDIA_ROOT, dir1)
            if not os.path.exists(dir):
                os.makedirs(dir)
            file_name = ext[0] + datetime.today().strftime("%Y%m%d%H%M%S") + str(randint(1, 1000)) + ext[1] if len(ext) > 1 else ''
            path = os.path.join(dir, file_name)
            dir2 = os.path.join(dir1, file_name)
            brand.logo = 'upload/' + dir2
        with open(path, 'wb') as fp:
            if file.multiple_chunks():
                for block1 in file.chunks():
                    fp.write(block1)
            else:
                fp.write(file.read())
        brand.yn = request.POST['checkbox']
        brand.category = TbCategory.objects.filter(id=request.POST['s_cid'])[0]
        brand.save()
        return redirect(reverse('backmanage:brand_manage'))

    return render(request, 'backmanage/Add_Brand.html', context={'all_big_category': all_big_category, 'all_small_category':  all_small_category})


def admin_competence(request):
    number = Privilege.objects.count()
    privilege = []
    privileges = Privilege.objects.all()
    for p in privileges:

        privilege.append({'privilege': p, 'users': p.admin.values('admin_name'), 'usercount':p.admin.count()})

    return render(request, 'backmanage/admin_Competence.html', context={'number': number, 'privilege': privilege})


def admin_info(request):
    if request.method == 'POST':
        oldpwd = request.POST.get('oldpwd')
        oldpassword_hash = hashlib.sha1(oldpwd.encode('utf8')).hexdigest()

        newpwd = request.POST.get('newpwd')
        newpassword_hash = hashlib.sha1(newpwd.encode('utf8')).hexdigest()

        confirm_newpwd = request.POST.get('confirm_newpwd')
        confirm_pwd = hashlib.sha1(confirm_newpwd.encode('utf8')).hexdigest()

        res = Admin.objects.filter(admin_name=request.session.get('admin_username')).update(admin_password=newpassword_hash)
        print(oldpwd, oldpassword_hash, newpwd, newpassword_hash, confirm_newpwd, confirm_pwd, res)
        return JsonResponse({'code': 1, 'msg': 'ok'}, safe=False)

    admin_name = request.session.get('admin_username')
    info = Admin.objects.get(admin_name=request.session.get('admin_username'))
    return render(request, 'backmanage/admin_info.html', context={'admin_name': admin_name, 'info': info})


def administrator(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        userpassword = request.POST.get('password')
        userpassword_hash = hashlib.sha1(userpassword.encode('utf8')).hexdigest()
        user_sex = request.POST.get('form-field-radio')
        login_ip = request.META['REMOTE_ADDR']
        user_tel = request.POST.get('user-tel')
        email = request.POST.get('email')
        user_qq = request.POST.get('user-qq')
        privilege = Privilege.objects.filter(id=request.POST.get('admin-role'))[0]
        reg_date = datetime.now()
        admin = Admin(admin_name=user_name, admin_password=userpassword_hash, admin_sex=user_sex, admin_phone=user_tel,
                      admin_email=email, admin_reg_date=reg_date, admin_login_ip=login_ip, admin_qq=user_qq,
                      privilege=privilege)
        admin.save()
        return JsonResponse({'code': 1, 'msg': 'ok'}, safe=False)
    admin_total = Admin.objects.count()
    admins = Admin.objects.all()
    privileges = Privilege.objects.all()
    return render(request, 'backmanage/administrator.html',
                  context={'admin_total': admin_total, 'admins': admins, 'privileges': privileges})


def ads_list(request):
    return render(request, 'backmanage/Ads_list.html')


@csrf_exempt
def advertising(request):
    if request.method == "POST":
        path = os.path.join(settings.MEDIA_ROOT, 'ad')
        print(request.POST)
        file = request.FILES.get('picture')
        path = os.path.join(path, file.name)
        # 创建新文件
        with open(path, 'wb') as fp:
            # 如果文件超过2.5M,则分块读写
            if file.multiple_chunks():
                for block1 in file.chunks():
                    fp.write(block1)
            else:
                fp.write(file.read())
        ad = Advertisement()
        ad.type = request.POST.get('class')
        ad.order = request.POST.get('order')
        ad.yn = request.POST.get('yn')
        ad.pic = 'upload/ad/' + file.name
        ad.save()
        return JsonResponse({'code': 0, 'msg': 'success'})
    ads = Advertisement.objects.order_by('id').all()
    return render(request, 'backmanage/advertising.html', context={'ad_list': ads})


def amount(request):
    return render(request, 'backmanage/Amounts.html')


def article_add(request):
    return render(request, 'backmanage/article_add.html')


def article_list(request):
    return render(request, 'backmanage/article_list.html')


def article_sort(request):
    return render(request, 'backmanage/article_Sort.html')


def brand_details(request,id=0):
    brands = TbBrand.objects.get(pk=id)
    return render(request, 'backmanage/Brand_detailed.html',context={'brands':brands})


def brand_manage(request):
    brands = TbBrand.objects.all()
    return render(request, 'backmanage/Brand_Manage.html',context={'brands':brands})


def category_manage(request):
    category = TbCategory.objects.values('id', 'name', 'parentid').filter(status=0).order_by('order').all()
    return render(request, 'backmanage/Category_Manage.html', context={'categorys': category})


def category_list(request):
    category = TbCategory.objects.filter(status=0).order_by('order').all()
    count = TbCategory.objects.filter(status=0).count()
    all_big_category = TbCategory.objects.filter(status=0, parentid=0).all()
    # todo 按照大类目分组显示小类目
    return render(request, 'backmanage/Category_list.html',
                  context={'categorys': category, 'count': count, 'all_big_category': all_big_category})


@csrf_exempt
def category_add(request):
    all_big_category = TbCategory.objects.filter(status=0, parentid=0).all()
    all_second_category = TbCategory.objects.filter(status=0).exclude(parentid=0).all()
    if request.method == "POST":
        category = TbCategory()
        category.name = request.POST['name']
        category.parentid = request.POST['parentid']
        category.order = request.POST['order']
        category.description = request.POST['description']
        category.save()
        # todo 增加小类目时，列表未更新
        return redirect(reverse('backmanage:category_list'))
    return render(request, 'backmanage/Category_add.html',
                  context={'all_big_category': all_big_category, 'all_second_category': all_second_category})


@csrf_exempt
def category_update(request, cid=None):
    if request.method == 'POST':
        category = TbCategory.objects.get(pk=request.POST.get('cid'))
        category.name = request.POST.get('name')
        category.parentid = request.POST.get('parentid')
        category.description = request.POST.get('description')
        category.order = request.POST.get('order')
        category.save()
        # todo 修改所属分类时，列表未更新
        return redirect(reverse('backmanage:category_list'))
    category = TbCategory.objects.get(pk=cid)
    all_big_category = TbCategory.objects.filter(status=0, parentid=0).all()
    # TODO  cid不存在时错误页面没有
    if not category:
        return HttpResponse("板块不存在")
    return render(request, 'backmanage/Category_update.html',
                  context={"category": category, 'all_big_category': all_big_category})


def competence(request, index=0):
    if index:
        privilege = Privilege.objects.get(pk=index)
        checked_admins = privilege.admin.all()
        print(privilege, checked_admins)
        admins = Admin.objects.all()
        return render(request, 'backmanage/Competence.html',
                      context={'admins': admins, 'checked_admins': checked_admins, 'privilege': privilege})
    if request.method == 'POST':
        if request.POST.get("privilege_id"):
            add_prv = Privilege.objects.get(pk=request.POST.get("privilege_id"))
        else:
            add_prv = Privilege()
        add_prv.privilege_name = request.POST.get('privilege_name')
        add_prv.describe = request.POST.get('describe')
        add_prv.menu_list = request.POST.getlist('user-Character-0-0')
        add_prv.save()
        user = request.POST.getlist('username')
        for u in user:

            Admin.objects.filter(id=int(u)).update(privilege=add_prv)
        return JsonResponse({'code':0, 'msg':'success'})
    admins = Admin.objects.all()
    return render(request, 'backmanage/Competence.html',context={'admins':admins,})


def cover_management(request):
    return render(request, 'backmanage/Cover_management.html')


def feedback(request):
    return render(request, 'backmanage/Feedback.html')


def guestbook(request):
    return render(request, 'backmanage/Guestbook.html')


def home(request):
    date = datetime.now()
    ip = request.META['REMOTE_ADDR']
    return render(request, 'backmanage/home.html', context={'date': date, 'ip': ip})


def integration(request):
    user = User.objects.all()
    user_total = User.objects.count()
    return render(request, 'backmanage/integration.html', context={'user': user, 'user_total': user_total})


def member_grading(request):
    user = User.objects.all()
    user_total = User.objects.count()
    return render(request, 'backmanage/member-Grading.html', context={'user': user, 'user_total': user_total})


def member_show(request, type):
    user = User.objects.all()
    if int(type) == 0:
        user = user.all()
    elif int(type) == 1:
        user = user.filter(grade__lt=1000)
    elif int(type) == 2:
        user = user.filter(grade__gte=1000, grade__lt=2500)
        print(user.query)
    elif int(type) == 3:
        user = user.filter(grade__gte=2500, grade__lt=5000)
    elif int(type) == 4:
        user = user.filter(grade__gte=5000, grade__lt=10000)
    else:
        user = user.filter(grade__gte=10000)
    return render(request, 'backmanage/member-Grading.html', context={'user': user})


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


@csrf_exempt
def product_add(request):
    all_big_category = TbCategory.objects.filter(status=0, parentid=0).all()
    all_small_category = TbCategory.objects.filter(~Q(parentid=0) & Q(status=0)).all()
    if request.method == 'POST':
        pictures = request.FILES.getlist('pictures')
        spu = TbSpu()
        spu.title = request.POST.get('title')
        spu.detail = request.POST.get('content')
        spu.brand = TbBrand.objects.get(pk=request.POST.get('brandid'))
        spu.category = TbCategory.objects.get(pk=request.POST.get('s_cid'))
        spu.unique_code = request.POST.get('unique_code')
        spu.list_pirce = request.POST.get('list_pirce')
        spu.save()
        paths = upload_pictures(spu.unique_code, pictures)
        for path in paths:
            spu_pic = TbSpuPics()
            spu_pic.spu = spu
            spu_pic.pic = path
            spu_pic.save()
        return redirect(reverse('backmanage:sku_add',
                                kwargs={'bcid': request.POST.get('b_cid'), 'scid': request.POST.get('s_cid'),
                                        'unique_code': spu.unique_code}))
    return render(request, 'backmanage/Product_add.html',
                  context={'all_small_category': all_small_category, 'all_big_category': all_big_category})


def upload_pictures(spuid, pictures):
    paths = []
    for picture in pictures:
        try:
            path = os.path.join(settings.STATIC_ROOT, str(spuid))
        except Exception as e:
            path = os.path.join(settings.MEDIA_ROOT, str(spuid))
        # 文件类型过滤
        ext = os.path.splitext(picture.name)
        if len(ext) < 1 or not ext[1] in settings.ALLOWED_FILEEXTS:
            return redirect(reverse('backmanage:product_add'))

        # 解决文件重名
        if not os.path.exists(path):
            os.makedirs(path)  # 递归创建目录
        path = os.path.join(path, picture.name)
        paths.append('upload/' + str(spuid) + '/' + picture.name)
        # 创建新文件
        with open(path, 'wb') as fp:
            # 如果文件超过2.5M,则分块读写
            if picture.multiple_chunks():
                for block1 in picture.chunks():
                    fp.write(block1)
            else:
                fp.write(picture.read())
    return paths


@csrf_exempt
def sku_add(request, bcid=None, scid=None, unique_code=None):
    all_big_category = TbCategory.objects.filter(status=0, parentid=0).all()
    all_small_category = TbCategory.objects.filter(~Q(parentid=0) & Q(status=0)).all()
    if request.method == 'POST':
        unique_code = request.POST.get('unique_code')
        spu = TbSpu.objects.get(unique_code=unique_code)
        print(request.POST.get('data'))
        for data in json.loads(request.POST.get('data')):
            sku = TbSku()
            sku.title = data['title']
            sku.price = data["price"]
            sku.total_amount = data['store']
            sku.spu = TbSpu.objects.get(unique_code=unique_code)
            sku.save()
            attrs = data['attribute'].split(',')
            print(attrs)
            for attr in attrs:
                attr_key = attr.split(':')[0]
                attr_value = attr.split(':')[1]
                sku_attr = TbSkuAttr()
                sku_attr.sku = sku
                sku_attr.attr_key = TbAttributeKey.objects.get(pk=attr_key)
                sku_attr.attr_value = TbAttributeValue.objects.get(pk=attr_value)
                sku_attr.save()
        return JsonResponse({'code': 0})
    return render(request, 'backmanage/Sku_add.html', context={'all_small_category': all_small_category,
                                                               'all_big_category': all_big_category,
                                                               'bcid': bcid, 'scid': scid, 'unique_code': unique_code})


def pruduct_list(request):
    # if request.method == 'POST':

    category = TbCategory.objects.values('id', 'name', 'parentid').filter(status=0).order_by('order').all()
    sku_list = TbSku.objects.all()
    skus = []
    for sku in sku_list:
        skus.append({'sku': sku, 'unique_code': sku.spu.unique_code})
    return render(request, 'backmanage/Products_List.html', context={'categorys': category, 'sku_list': skus})


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


def user_list(request):  # 会员列表
    # del = User.objects.get(pk)
    # del.delete()
    user = User.objects.all()
    user_total = User.objects.count()
    return render(request, 'backmanage/user_list.html', context={'user': user, 'user_total': user_total})


def attribute_list(request, cid):
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
    return render(request, 'backmanage/Attribute_list.html',
                  context={'common_attribute': common_attribute, 'special_attribute': special_attribute, 'cid': cid})


@csrf_exempt
def attribute_update(request):
    if request.method == 'POST' and request.is_ajax():
        value_id = request.POST.get('value_id')
        value = request.POST.get("value")
        attribute_value = TbAttributeValue.objects.get(pk=value_id)
        if attribute_value.attr.attr_value.filter(value=value).exists():
            return JsonResponse({'code': 1, 'msg': '属性已存在'})
        attribute_value.value = value
        attribute_value.save()
        return JsonResponse({'code': 0})
    return JsonResponse({'code': 1, 'msg': '未知错误,请刷新重试'})


def attribute_delete(request):
    return None


def attribute_add(request):
    if request.method == 'POST' and request.is_ajax():
        cid = request.POST.get('cid')
        category = TbCategory.objects.get(pk=cid)
        is_common = request.POST.get('is_common')
        attribute_name = request.POST.get("attribute_name")
        attribute_value = request.POST.get("attribute_value")
        if is_common is None or attribute_value is None or attribute_name is None or attribute_name.strip() == '' or attribute_value.strip() == '':
            return JsonResponse({'code': 1, 'msg': '参数错误'})
        if is_common == '1':
            res = category.attr_key.filter(is_common=1, name=attribute_name.strip())
            if res.exists():
                return JsonResponse({'code': 1, 'msg': '属性已存在'})
            common_attribute = TbAttributeKey()
            common_attribute.is_common = 1
            common_attribute.category = category
            common_attribute.name = attribute_name.strip()
            common_attribute.save()
            common_attribute_value = TbAttributeValue()
            common_attribute_value.value = attribute_value.strip()
            common_attribute_value.attr = common_attribute
            common_attribute_value.save()
            return JsonResponse({'code': 0, 'msg': 'success'})
        if is_common == '0':
            res = category.attr_key.filter(is_common=0, name=attribute_name.strip())
            if res.exists():
                attribute_values = res[0].attr_value.filter(value=attribute_value)
                if attribute_values.exists():
                    return JsonResponse({'code': 1, 'msg': '属性已存在'})
                else:
                    special_attribute_value = TbAttributeValue()
                    special_attribute_value.attr = res[0]
                    special_attribute_value.value = attribute_value
                    special_attribute_value.save()
                    return JsonResponse({'code': 0, 'msg': 'success'})
            else:
                special_attribute = TbAttributeKey()
                special_attribute.is_common = 0
                special_attribute.category = category
                special_attribute.name = attribute_name.strip()
                special_attribute.save()
                special_attribute_value = TbAttributeValue()
                special_attribute_value.attr = special_attribute
                special_attribute_value.value = attribute_value
                special_attribute_value.save()
                return JsonResponse({'code': 0, 'msg': 'success'})
    return JsonResponse({'code': 1, 'msg': '请求方式错误'})


def logout(request):
    request.session.pop('admin_id')
    request.session.pop('admin_username')
    return redirect(reverse('backmanage:login'))


def verficode(request):
    vc = VerfiCode()
    res = vc.output()
    request.session['admin_verficode'] = vc.code
    return HttpResponse(res)


def attribute_get(request):
    cid = request.GET.get('cid')
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
    brands = []
    data = category.brand.all()
    for brand in data:
        brands.append({"id": brand.id, "name": brand.name})
    return JsonResponse(
        {'common_attribute': common_attribute, 'special_attribute': special_attribute, 'cid': cid, 'brand': brands})


@csrf_exempt
def delete(request):
    del_id = request.POST.get('id')
    cut = User.objects.get(pk=del_id)
    cut.delete()
    return JsonResponse('删除成功')


@csrf_exempt
def delete_all(request):
    delall_id = request.POST.get('ids')
    for i in delall_id.split(","):
        cutall = User.objects.get(pk=i)
        cutall.delete()
    return JsonResponse('批量删除成功')


def update_advertising(request):
    yn = request.GET.get('yn')
    ad = Advertisement.objects.get(pk=request.GET.get('id'))
    ad.yn = yn
    ad.save()
    return JsonResponse({'code': 0})


def del_advertising(request):
    ad = Advertisement.objects.get(pk=request.GET.get('id'))
    ad.delete()
    return JsonResponse({'code': 0})