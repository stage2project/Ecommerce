from django.db import models


class TbCategory(models.Model):
    """
    商品分类模型
    主要参数：商品名称，父分类id，状态，显示顺序，创建时间
    """
    name = models.CharField(max_length=40)
    parentid = models.IntegerField()
    status = models.SmallIntegerField(default=0)
    order = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, default=None, null=True)

    class Meta:
        db_table = 'tb_category'

    def __str__(self):
        return self.name


class TbBrand(models.Model):
    """
    商品品牌模型
    名称，logo，是否有效，所属分类
    """
    name = models.CharField(max_length=40)
    logo = models.CharField(max_length=100)
    yn = models.IntegerField()
    category = models.ForeignKey('TbCategory', models.DO_NOTHING, db_column='cid', related_name='brand')

    class Meta:
        db_table = 'tb_brand'


class TbAttributeKey(models.Model):
    """
    商品属性名称表：
    名称，分类，创建时间，是否是通用属性，默认不同用，是否有效
    """
    name = models.CharField(max_length=30, blank=True, null=True)
    category = models.ForeignKey('TbCategory', models.DO_NOTHING, db_column='cid', blank=True, null=True, related_name='attr_key')
    create_time = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    is_common = models.IntegerField(default=0)
    yn = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        db_table = 'tb_attribute_key'


class TbAttributeValue(models.Model):
    """
        商品属性值表：
        值，所属键id，创建时间，是否有效
        """
    value = models.CharField(max_length=30, blank=True, null=True)
    attr = models.ForeignKey('TbAttributeKey', models.DO_NOTHING, db_column='attr_key_id', blank=True, null=True, related_name='attr_value')
    create_time = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    yn = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        db_table = 'tb_attribute_value'


class TbSpu(models.Model):
    """
    商品表；商品唯一编码，分类，品牌，详细内容，状态，创建时间，列表价格
    """
    unique_code = models.IntegerField(unique=True, blank=True, primary_key=True)
    category = models.ForeignKey(TbCategory, models.DO_NOTHING, db_column='cid', related_name='spus')
    brand = models.ForeignKey('TbBrand', models.CASCADE, db_column='bid', related_name='spus')
    title = models.CharField(max_length=100, blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True, default=0)
    create_time = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    list_pirce = models.FloatField(default=0)

    class Meta:
        db_table = 'tb_spu'


class TbSku(models.Model):
    """
    具体商品表：所属商品分类，价格，状态，创建时间，总数量，已售数量
    """
    spu = models.ForeignKey('TbSpu', models.DO_NOTHING, db_column='unique_code', blank=True, null=True, related_name='skus')
    title = models.CharField(max_length=100, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True, default=0)
    create_time = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    total_amount = models.IntegerField(blank=True, null=True)
    sold_amount = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'tb_sku'


class TbSpuPics(models.Model):
    """商品展示图表
    商品id，图像路径，是否是默认图片
    """
    spu = models.ForeignKey(TbSpu, models.CASCADE, db_column='spu_id', related_name='spu_pic')
    pic = models.CharField(max_length=1000, blank=True, null=True)
    is_default = models.IntegerField(blank=True, null=True, default=0)
    order = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        db_table = 'tb_spu_pics'


class TbSkuAttr(models.Model):
    sku = models.ForeignKey('TbSku', models.CASCADE, db_column='sku_id', related_name='sku_attr')
    attr_key = models.ForeignKey('TbAttributeKey', models.CASCADE, db_column='attr_key_id', related_name='sku_attr')
    attr_value = models.ForeignKey('TbAttributeValue', models.CASCADE, db_column='attr_value_id', related_name='sku_attr')

    class Meta:
        db_table = "tb_sku_attr"


class TbSpuAttr(models.Model):
    spu = models.ForeignKey('TbSpu', models.CASCADE, db_column='unique_code', related_name='spu_attr')
    attr_key = models.ForeignKey('TbAttributeKey', models.CASCADE, db_column='attr_key_id', related_name='spu_attr')
    attr_value = models.ForeignKey('TbAttributeValue', models.CASCADE, db_column='attr_value_id', related_name='spu_attr')

    class Meta:
        db_table = "tb_spu_attr"


class TbCategoryPics(models.Model):
    """商品展示图表
    商品id，图像路径，是否是默认图片
    """
    category = models.ForeignKey(TbCategory, models.CASCADE, db_column='cid', related_name='category_pic')
    pic = models.CharField(max_length=1000, blank=True, null=True)
    yn = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tb_category_pics'
