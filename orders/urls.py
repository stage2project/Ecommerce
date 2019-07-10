from django.conf.urls import url, include

from orders import views

urlpatterns = [
    url(r'^confirm_order/$', views.confirm_order, name='confirm_order'),
    url(r'^commit_order/$', views.commit_order, name='commit_order'),
]
