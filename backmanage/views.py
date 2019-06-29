from datetime import datetime

from django.shortcuts import render


# Create your views here.
def index(request):
    date = datetime.now()
    return render(request, 'index.html',context={'date':date})


def login(request):
    return render(request, 'login.html')


def account_detail(request):
    return render(request, 'Account_Details.html')


def add_brand(request):
    return render(request, 'Add_Brand.html')


def admin_competence(request):
    return render(request, 'admin_Competence.html')


def info(request):
    return render(request, 'admin_info.html')


def administrator(request):
    return render(request, 'administrator.html')


def ads_list(request):
    return render(request, 'Ads_list.html')


def advertising(request):
    return render(request, 'advertising.html')


def amount(request):
    return render(request, 'Amounts.html')


def article_add(request):
    return render(request, 'article_add.html')


def article_list(request):
    return render(request, 'article_list.html')


def article_sort(request):
    return render(request, 'article_Sort.html')


def brand_details(request):
    return render(request, 'Brand_detailed.html')


def brand_manage(request):
    return render(request, 'Brand_Manage.html')


def category_manage(request):
    return render(request, 'Category_Manage.html')


def competence(request):
    return render(request, 'Competence.html')


def cover_management(request):
    return render(request, 'Cover_management.html')


def feedback(request):
    return render(request, 'Feedback.html')


def guestbook(request):
    return render(request, 'Guestbook.html')


def home(request):
    date = datetime.now()
    ip = request.META['REMOTE_ADDR']
    return render(request, 'home.html', context={'date':date,'ip':ip})


def integration(request):
    return render(request, 'integration.html')


def member_grading(request):
    return render(request, 'member-Grading.html')


def member_show(request):
    return render(request, 'member-show.html')


def order_chart(request):
    return render(request, 'Order_Chart.html')


def order_detailed(request):
    return render(request, 'order_detailed.html')


def order_handling(request):
    return render(request, 'Order_handling.html')


def orderform(request):
    return render(request, 'Orderform.html')


def payment_configure(request):
    return render(request, 'Payment_Configure.html')


def payment_detail(request):
    return render(request, 'Payment_details.html')


def payment_method(request):
    return render(request, 'payment_method.html')


def picture_add(request):
    return render(request, 'picture-add.html')


def product_category_add(request):
    return render(request, 'product-category-add.html')


def pruduct_list(request):
    return render(request, 'Products_List.html')


def refund(request):
    return render(request, 'Refund.html')


def refund_detailed(request):
    return render(request, 'Refund_detailed.html')


def shop_list(request):
    return render(request, 'Shop_list.html')


def shopping_detailed(request):
    return render(request, 'shopping_detailed.html')


def shops_audit(request):
    return render(request, 'Shops_Audit.html')


def sort_ads(request):
    return render(request, 'Sort_ads.html')


def system_logs(request):
    return render(request, 'System_Logs.html')


def system_section(request):
    return render(request, 'System_section.html')


def systems(request):
    return render(request, 'Systems.html')


def transaction(request):
    return render(request, 'transaction.html')


def user_list(request):
    return render(request, 'user_list.html')
