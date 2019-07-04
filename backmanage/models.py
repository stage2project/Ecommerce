from datetime import datetime

from django.db import models

# Create your models here.

class PayMethod(models.Model):
    name = models.CharField(max_length=60, null=False)
    logo = models.CharField(max_length=100, null=False)
    type = models.IntegerField()
    yn = models.SmallIntegerField()
    create_time = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'pay_method'


class Advertisement(models.Model):
    pic = models.CharField(max_length=100, null=False)
    yn = models.SmallIntegerField()
    order = models.SmallIntegerField()
    create_time = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'advertisement_info'


class Admin(models.Model):                                               # admin 管理员表建模
    admin_name = models.CharField(max_length=255,unique=True)            # 管理员姓名
    admin_password = models.CharField(max_length=128)    # 管理员密码
    admin_sex = models.BooleanField(default=True)
    admin_age = models.IntegerField(default=0)
    admin_reg_date = models.DateTimeField(max_length=32)                 #注册时间
    admin_login_ip = models.CharField(max_length=32)                     #登录ip
    admin_login_addr = models.CharField(max_length=32)                   #登陆地点
    status = models.BooleanField(default=True)
    admin_email = models.CharField(max_length=255)                       # 管理员电子邮箱
    admin_phone = models.CharField(max_length=11)                       # 管理员电话号码
    admin_qq = models.CharField(max_length=16)
    privilege = models.ForeignKey('Privilege', on_delete=models.CASCADE, db_column='privilege_id', related_name='admin')

    class Meta:
        db_table = 'admin'                                               # 表名admin


class Privilege(models.Model):
    privilege_name = models.CharField(max_length=255)              # 权限名称
    describe = models.CharField(max_length=255, null=True)         # 权限描述
    menu_list = models.CharField(max_length=255)                   # 权限名字

    class Meta:
        db_table = 'privilege'                                     # 表名为privilege
