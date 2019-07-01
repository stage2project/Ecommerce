import hashlib

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from users.models import User


def index(request):
    return HttpResponse('index')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password = hashlib.sha1(password.encode('utf8')).hexdigest()
        print(username, password)
        # 查询数据库
        res = User.objects.filter(username=username, password=password).values('username', 'id')
        print(res[0])
        if len(res) > 0:
            # response = HttpResponseRedirect(reverse('index'))
            # response = redirect(reverse('index'))
            # response.set_cookie('uid', res[0]['id'], max_age=3600)
            # response.set_cookie('username', res[0]['username'], max_age=3600)
            # response.set_signed_cookie('username', res[0]['username'], salt=SECRET_KEY)
            # return response

            # session
            request.session['uid'] = res[0]['id']
            request.session['username'] = res[0]['username']
            return render(request, 'goods/index.html')
    return render(request, 'goods/login.html')


def register(request):
    return render(request, 'goods/register.html')


