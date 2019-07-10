from django.urls import reverse

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class MiddleWareCus1(MiddlewareMixin):

    def process_request(self, request):
        need_login_url_list = ['/person/', '/address_manage/', '/evaluation_manage/', '/order_manage/', '/collection_manage/', '/order_info/', '/add_cart/', '/cart_manage/']
        if request.path in need_login_url_list:
            if not request.session.get('uid'):
                return redirect(reverse('users:login'))

