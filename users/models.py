from datetime import datetime

from django.db import models

# Create your models here.
from django.forms import forms


class User(models.Model):                                          # user 用户表建模
    username = models.CharField(max_length=255, null=False)        # 姓名
    password = models.CharField(max_length=128, null=False)        # 密码
    sex = models.SmallIntegerField(default=2, null=True)                           # 性别（0=男，1=女，2=保密）
    birthday = models.DateField(null=True, default=datetime.now)              # 生日
    email = models.CharField(max_length=255, null=False)           # 电子邮箱
    picture = models.CharField(max_length=255, null=True)          # 头像
    phone = models.CharField(max_length=255, null=False)           # 电话号码
    place = models.CharField(max_length=255, null=True)            # 所在地
    grade = models.CharField(max_length=255, default=0)            # 积分
    problem = models.CharField(max_length=255, null=True)          # 问题
    answer = models.CharField(max_length=255, null=True)           # 答案
    regtime = models.DateField(default=datetime.now)               # 创建时间
    islogin = ((1, '允许登录'), (2, '禁止登录'))                      # 自定义类型对应mysql的enum类型
    allowed = models.IntegerField(default=1, choices=islogin)      # 默认是 1-允许登录

    class Meta:
        db_table = 'user'                                          # 表名user


class Admin(models.Model):                                         # admin 管理员表建模
    admin_name = models.CharField(max_length=255, null=False)      # 管理员姓名
    admin_password = models.CharField(max_length=128, null=False)  # 管理员密码
    admin_email = models.CharField(max_length=255, null=False)     # 管理员电子邮箱
    admin_phone = models.CharField(max_length=255, null=False)     # 管理员电话号码
    privilege = models.ForeignKey('Privilege', db_column='privilege_id', related_name='admin')

    class Meta:
        db_table = 'admin'                                         # 表名admin


class Privilege(models.Model):
    privilege_name = models.CharField(max_length=255)              # 权限名称
    describe = models.CharField(max_length=255, null=True)         # 权限描述
    menu_list = models.CharField(max_length=255)                     # 权限名字

    class Meta:
        db_table = 'privilege'                                     # 表名为privilege


class Address(models.Model):                                       # address 收货地址建模
    a_name = models.CharField(max_length=255)                      # 收件人姓名
    a_phone = models.CharField(max_length=128)                     # 收件人电话
    a_place = models.CharField(max_length=255, null=False)         # 收货地址
    a_email = models.CharField(max_length=255, null=False)         # 收件人邮箱

    class Meta:
        db_table = 'address'                                       # 表名address





