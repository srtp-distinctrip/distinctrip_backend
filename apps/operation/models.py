from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from scenic.models import Scenic
from article.models import Article

User = get_user_model()

# Create your models here.


class UserFav(models.Model):
    """
    用户收藏
    """
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    article = models.ForeignKey(Article, verbose_name="路书", on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class UserLeavingMessage(models.Model):
    """
    用户评论
    """
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    article = models.ForeignKey(Article, verbose_name="路书", on_delete=models.CASCADE)
    message = models.TextField(default="", verbose_name="内容", help_text="内容")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message


class Questionnaire(models.Model):
    """
    问卷
    """
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    choose = models.CharField(max_length=6, choices=(("A", "A"), ("B", "B"), ("C", "C")), default="N", verbose_name="问卷")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "问卷"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


class Route(models.Model):
    """
    路线
    """
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(Questionnaire, blank=True, null=True, verbose_name="问卷", on_delete=models.CASCADE)
    route = models.TextField(default="路线", verbose_name="路线")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "路线"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id
