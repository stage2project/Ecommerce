from django.conf.urls import url

from users import views

urlpatterns = [

    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^person/$', views.person, name='person'),
    url(r'^order/$', views.order, name='order'),
    url(r'^collect/$', views.collect, name='collect'),
    url(r'^sale/$', views.sale, name='sale'),
    url(r'^retreat/$', views.retreat, name='retreat'),

    # url(r'^sms/$', views.send_sms, name='sms'),

]
