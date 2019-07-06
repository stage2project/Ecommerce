import re
from django import forms
from django.core.exceptions import ValidationError
from .models import User


class UserRegisterForm(forms.Form):
    username = forms.CharField(min_length=3, error_messages={
        'required': '必须输入用户名',
        'min_length': '用户名不能少于3位'
    })
    password = forms.CharField(min_length=6, error_messages={
        'required': '必须输入密码',
        'min_length': '密码长度不能小于6位'
    })
    confirm_password = forms.CharField(min_length=6, error_messages={
        'required': '必须输入密码',
        'min_length': '密码长度不能小于6位'
    })
    email = forms.CharField(error_messages={
        'required': '必须输入邮箱',
    })
    phone = forms.CharField(max_length=11, error_messages={
        'required': '必须输入手机号码',
        'max_length': '电话号码不能大于11位'
    })
    # sms = forms.CharField(max_length=6)

    def clean_username(self):
        res = User.objects.filter(username=self.cleaned_data.get('username')).exists()
        if res:
            raise ValidationError("用户名重名")
        return self.cleaned_data.get('username')

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        if re.match(r'\d+$', pwd):
            raise ValidationError("密码不能是纯数字")
        return pwd

    def clean(self):
        pwd1 = self.cleaned_data.get('password')
        pwd2 = self.cleaned_data.get('confirm_password')
        if pwd2 != pwd1:
            raise ValidationError({'confirm_password': "两次密码不一致"})
        return self.cleaned_data

    def clean_email(self):
        res1 = User.objects.filter(email=self.cleaned_data.get('email')).exists()
        if res1:
            raise ValidationError('邮箱重复')
        email = self.cleaned_data.get('email')
        if email:
            if not re.match(r'^\w+((.\w+)|(-\w+))@[A-Za-z0-9]+((.|-)[A-Za-z0-9]+).[A-Za-z0-9]+$', email):
                raise ValidationError('邮箱格式不正确')
        return self.cleaned_data.get('email')

    def clean_phone(self):
        res2 = User.objects.filter(phone=self.cleaned_data.get('phone')).exists()
        if res2:
            raise ValidationError('手机号码重复')
        phone = self.cleaned_data.get('phone')
        if phone:
            if not re.match(r'^1[3456789]\d{9}$', phone):
                raise ValidationError('手机格式不正确')
        return self.cleaned_data.get('phone')




