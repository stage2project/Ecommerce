from django.db import models

# Create your models here.
# class Administrator(models.Model):



# class BkCategory(models.Model):
#     """
#     商品分类模型
#     主要参数：商品名称，父分类id，状态，显示顺序，创建时间
#     """
#     name = models.CharField(max_length=40)
#     parentid = models.IntegerField()
#     status = models.SmallIntegerField()
#     order = models.IntegerField()
#     create_time = models.DateTimeField()
#
#     class Meta:
#         db_table = 'bk_category'