from django.db import models

# Create your models here.


class CartInfo(models.Model):
    user = models.ForeignKey('users.User', verbose_name='用户')
    product = models.ForeignKey('goods.TbSku', verbose_name='商品SKU')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总价')
    product_count = models.IntegerField(verbose_name='商品数量')

    class Meta:
        db_table = 'cart_info'
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name