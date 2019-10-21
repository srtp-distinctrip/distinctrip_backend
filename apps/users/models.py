from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserProfile(AbstractUser):
    """
    用户信息表
    """
    # UserProfile是继承了Django自带的一个AbstractUser类
    # 下面是UserProfile相对于AbstractUser新增的一些字段
    # name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=(("male", "男"), ("female", "女")), default="female",
                              verbose_name="性别")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="电话")
    # email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    短信验证码表（验证码实际上也可以保存到内存中（例如Redis））
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="电话")
    # datetime.now()是项目启动时间，datetime.now才是真正的当前时间
    # 很多字段都会有add_time、updata_time、和delete_time（因为很多不是真删，只是做一个标记）
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
