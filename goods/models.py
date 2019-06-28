# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class TbAttributeKey(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    cid = models.ForeignKey('TbCategory', models.DO_NOTHING, db_column='cid', blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    yn = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_attribute_key'


class TbAttributeValue(models.Model):
    value = models.CharField(max_length=30, blank=True, null=True)
    attr = models.ForeignKey(TbAttributeKey, models.DO_NOTHING, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    yn = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_attribute_value'


class TbBrand(models.Model):
    name = models.CharField(max_length=40)
    logo = models.CharField(max_length=100)
    yn = models.IntegerField()
    cid = models.ForeignKey('TbCategory', models.DO_NOTHING, db_column='cid')

    class Meta:
        managed = False
        db_table = 'tb_brand'


class TbCategory(models.Model):
    name = models.CharField(max_length=40)
    parentid = models.IntegerField()
    status = models.SmallIntegerField()
    order = models.IntegerField()
    create_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tb_category'


class TbSku(models.Model):
    spu_id = models.ForeignKey('TbSpu', models.DO_NOTHING, db_column='spu_id', blank=True, null=True, related_name='skus')
    attr_json = models.CharField(max_length=1000, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    total_amount = models.IntegerField(blank=True, null=True)
    sold_amount = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_sku'


class TbSkuPics(models.Model):
    sku = models.ForeignKey(TbSku, models.DO_NOTHING)
    pic = models.CharField(max_length=1000, blank=True, null=True)
    is_default = models.IntegerField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_sku_pics'


class TbSpu(models.Model):
    unique_code = models.IntegerField(unique=True, blank=True, null=True)
    cid = models.ForeignKey(TbCategory, models.DO_NOTHING, db_column='cid')
    title = models.CharField(max_length=100, blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_spu'
