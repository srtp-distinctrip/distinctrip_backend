from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

# Create your models here.


class Scenic(models.Model):
    """
    景点
    """
    name = models.CharField(max_length=100, verbose_name="景点名称")
    scenic_sn = models.CharField(max_length=50, default="xxx", verbose_name="景点编号")
    lable = models.TextField(default="标签", verbose_name="景点标签")
    province = models.CharField(max_length=20, verbose_name="所在省份")
    city = models.CharField(max_length=20, verbose_name="所在城市")
    address = models.CharField(max_length=100, verbose_name="详细地址")
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    visit_num = models.IntegerField(default=0, verbose_name="历史旅游人数")
    fav_num = models.IntegerField(default=0, verbose_name="收藏数")
    price = models.FloatField(default=0, verbose_name="平均消费")
    scenic_brief = models.TextField(max_length=500, verbose_name="景点简短描述")
    scenic_desc = UEditorField(verbose_name=u"景点详细描述", imagePath="scenic/images/", width=1000, height=300,
                              filePath="scenic/files/", default='')
    is_ticket = models.BooleanField(default=False, verbose_name="是否需要门票")
    scenic_front_image = models.ImageField(upload_to="scenic/images/", null=True, blank=True, verbose_name="封面图")
    is_recommend = models.BooleanField(default=False, verbose_name="是否推荐", help_text="是否推荐")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '景点'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ScenicImage(models.Model):
    """
    景点轮播图
    """
    scenic = models.ForeignKey(Scenic, verbose_name="景点", related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="scenic/images", verbose_name="图片", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '景点图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.scenic.name


class Banner(models.Model):
    """
    轮播的商品
    """
    scenic = models.ForeignKey(Scenic, verbose_name="景点", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banner', verbose_name="轮播图片")
    index = models.IntegerField(default=0, verbose_name="轮播顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '轮播景点'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.scenic.name


class HotSearchWords(models.Model):
    """
    热搜词
    """
    keywords = models.CharField(max_length=20, default="热搜词", verbose_name="热搜词")
    index = models.IntegerField(default=0, verbose_name="排序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '热搜词'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords
