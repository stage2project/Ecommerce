from datetime import datetime

from django.shortcuts import render


# Create your views here.
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


def info(request):
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
