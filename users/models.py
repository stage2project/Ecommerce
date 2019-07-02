from datetime import datetime

from django.db import models

# Create your models here.


class User(models.Model):                                          # user 用户表建模
    username = models.CharField(max_length=255, null=False)        # 姓名
    password = models.CharField(max_length=128, null=False)        # 密码
    sex = models.BooleanField(default=0)                           # 性别（0=男，1=女，2=保密）
    birthday = models.DateField(default=datetime.now)              # 生日
    email = models.CharField(max_length=255, null=False)           # 电子邮箱
    picture = models.CharField(max_length=255, null=True)          # 头像
    phone = models.CharField(max_length=255, null=False)           # 电话号码
    place = models.CharField(max_length=255, null=False)           # 所在地
    grade = models.CharField(max_length=255, default=0)            # 积分
    problem = models.CharField(max_length=255, null=True)          # 问题
    answer = models.CharField(max_length=255, null=True)           # 答案
    regtime = models.DateField(default=datetime.now)               # 创建时间
    islogin = ((1, '允许登录'), (2, '禁止登录'))                      # 自定义类型对应mysql的enum类型
    allowed = models.IntegerField(default=1, choices=islogin)      # 默认是 1-允许登录

    class Meta:
        db_table = 'user'                                          # 表名user


class Address(models.Model):                                       # address 收货地址建模
    a_name = models.CharField(max_length=255)                      # 收件人姓名
    a_phone = models.CharField(max_length=128)                     # 收件人电话
    a_place = models.CharField(max_length=255, null=False)         # 收货地址
    a_email = models.CharField(max_length=255, null=False)         # 收件人邮箱
    is_default = models.BooleanField(default=False, verbose_name='是否默认')  # 是否默认

    class Meta:
        db_table = 'address'                                       # 表名address


class UserFav(models.Model):
    user = models.ForeignKey('users.User', verbose_name='用户', related_name='user_fav')
    sku = models.ForeignKey('goods.TbSku', verbose_name='商品SKU')
    create_time = models.DateField(default=datetime.now)

    class Meta:
        db_table = 'user_fav'


class UserComment(models.Model):
    LEVEL = (
        (1, '好评'),
        (2, '中评'),
        (3, '差评'),
    )
    LEVEL_DIC = {
        '1': '好评',
        '2': '中评',
        '3': '差评',
    }
    user = models.ForeignKey('User', verbose_name='用户', related_name='user_comment')
    sku = models.ForeignKey('goods.TbSku', verbose_name='商品SKU')
    create_time = models.DateField(default=datetime.now)
    content = models.CharField(max_length=10000)
    pics = models.CharField(max_length=1000)
    score = models.IntegerField()
    level = models.SmallIntegerField(choices=LEVEL, default=1)

    class Meta:
        db_table = 'user_comment'
