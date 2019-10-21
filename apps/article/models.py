from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model
from DjangoUeditor.models import UEditorField

User = get_user_model()

# Create your models here.


class Article(models.Model):
    """
    路书
    """
    title = models.CharField(max_length=100, verbose_name="标题")
    author = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    article_sn = models.CharField(max_length=50, default="xxx", verbose_name="文章编号")
    lable = models.TextField(default="标签", verbose_name="文章标签")
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    fav_num = models.IntegerField(default=0, verbose_name="收藏数")
    article_brief = models.TextField(max_length=500, verbose_name="简短描述")
    article_desc = UEditorField(verbose_name=u"内容", imagePath="article/images/", width=1000, height=300,
                              filePath="article/files/", default='')
    article_front_image = models.ImageField(upload_to="scenic/images/", null=True, blank=True, verbose_name="封面图")
    is_recommend = models.BooleanField(default=False, verbose_name="是否推荐", help_text="是否推荐")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '路书'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
