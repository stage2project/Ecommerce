from django.conf.urls import url

from users import views

urlpatterns = [

    url(r'^login/$', views.login, name='login'),           # 登录
    url(r'^register/$', views.register, name='register'),  # 注册
    url(r'^person/$', views.person, name='person'),        # 我的商城
    url(r'^order/$', views.order, name='order'),           # 订单
    url(r'^collect/$', views.collect, name='collect'),     # 收藏
    url(r'^sale/$', views.sale, name='sale'),              #
    url(r'^retreat/$', views.retreat, name='retreat'),     # 退货
    url(r'^evaluation/$', views.evaluation, name='evaluation'),
    url(r'^address/$', views.address, name='address'),
]
