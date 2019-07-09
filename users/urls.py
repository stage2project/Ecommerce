from django.conf.urls import url

from users import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^person/$', views.person, name='person'),
    # url(r'^sms/$', views.send_sms, name='sms'),
    url(r'^address_manage/$', views.address_manage, name='address_manage'),
    url(r'^evaluation_manage/$', views.evaluation_manage, name='evaluation_manage'),
    url(r'^order_manage/$', views.order_manage, name='order_manage'),
    url(r'^collection_manage/$', views.collection_manage, name='collection_manage'),
    url(r'^order_info/$', views.order_info, name='order_info'),
    url(r'^logout/$', views.logout, name='logout'),
]
