from django.conf.urls import url

from users import views

urlpatterns = [

    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^person/$', views.person, name='person'),
    url(r'^sms/$', views.sms, name='sms'),

]
