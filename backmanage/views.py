import hashlib
from datetime import datetime

from django.contrib.messages.storage import session
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from backmanage.models import *


# Create your views here.


def add_competence(request):
    comp = {'超级管理员':'拥有至高无上的权利,操作系统的所有权限','普通管理员':'拥有网站系统大部分使用权限,无权限管理功能','编辑管理员':'拥有部分权限,主要进行编辑功能,无编辑订单功能,权限分配功能'}
    for key,value in comp.items():
        res = Privilege()
        res.privilege_name = key
        res.describe = value
        res.menu_list = [0]
        res.save()
    return HttpResponse('添加权限')


def add_admin(request):
    admin = Admin()
    admin.admin_name = '李晓妮'
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
    date = datetime.now()
    # id = session['id']
    # menu_list = Admin.objects.values('menu_list').get(pk=id)
    # [1,2,3]
    return render(request, 'backmanage/index.html',context={'date':date})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password = hashlib.sha1(password.encode('utf8')).hexdigest()
        print(username, password)
        res = Admin.objects.filter(admin_name=username,admin_password=password).values('username','id')
        if len(res)>0:  # 登录成功
            request.session['uid'] = res[0]['id']
            request.session['username'] = res[0]['username']
            return redirect(reverse('backmanage:index'))
    return render(request, 'backmanage/login.html')


def account_detail(request):
    return render(request, 'backmanage/Account_Details.html')


def add_brand(request):
    return render(request, 'backmanage/Add_Brand.html')


def admin_competence(request):
    return render(request, 'backmanage/admin_Competence.html')


def admin_info(request):
    # info = Admin.objects.get(admin_name = request.session.get('username'))
    # info.admin_sex
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
    return render(request, 'backmanage/Category_Manage.html')


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


def product_category_add(request):
    return render(request, 'backmanage/product-category-add.html')


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


