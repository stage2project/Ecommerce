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
