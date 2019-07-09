from django.conf.urls import url, include

from goods import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^details/(?P<spu_id>\d+)$', views.details, name='details'),
    url(r'^get_price/(?P<spu_id>\d+)$', views.get_price, name='get_price'),
    url(r'^list_page/(?P<cid>\d+)$', views.list_page, name='list_page'),
    url(r'^spu_filter/(?P<cid>\d+)$', views.spu_filter, name='spu_filter'),
    url(r'^cart_manage/$', views.cart_manage, name='cart_manage'),
    url(r'^add_cart/$', views.add_cart, name='add_cart'),
]
