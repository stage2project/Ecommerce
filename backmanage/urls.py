from django.conf.urls import url

from backmanage import views

urlpatterns = [
    url(r'^$', views.index, name='index')
]