from django.conf.urls import url

from users import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^person/$', views.person, name='person'),
    url(r'^sms/$', views.send_sms, name='sms'),
    url(r'^address_manage/$', views.address_manage, name='address_manage'),
    url(r'^evaluation_manage/$', views.evaluation_manage, name='evaluation_manage'),
    url(r'^order_manage/$', views.order_manage, name='order_manage'),
    url(r'^collection_manage/$', views.collection_manage, name='collection_manage'),
    url(r'^order_info/$', views.order_info, name='order_info'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^add_address/$', views.add_address, name='add_address'),
    url(r'^set_default_address/(?P<address_id>\d+)/$', views.set_default_address, name='set_default_address'),
    url(r'^edit_address/$', views.edit_address, name='edit_address'),
    url(r'^del_address/(?P<address_id>\d+)/$', views.del_address, name='del_address'),
]
