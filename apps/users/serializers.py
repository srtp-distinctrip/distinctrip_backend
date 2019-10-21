__author__ = 'dmxjhg'
__date__ = '2019/8/13 19:50'

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

import re
from datetime import datetime
from datetime import timedelta

from distinctrip_backend.settings import REGEX_MOBILE
from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    # 这里不继承ModelSerializer，因为在model设计时，code是必填字段
    # 如果用了ModelSerializer，就会将表单与VerifyCode做一个关联，则在点击发送验证码时，会报验证码必填的错
    # 所以继承Serializer自己写逻辑进行保存

    mobile = serializers.CharField(max_length=11)  # 有了这个声明，下面就可以针对这个mobile做一些检验了

    def validate_mobile(self, mobile):
        """
        验证手机号码
        """
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    # 这里继承了ModelSerializer，虽然code不是user的字段，但仍然可以
    # 一些技巧可以让我们既享受到ModelSerializer给我们带来的好处（不需要自己序列化），又突破它的一些限制
    # 和上面不同，这里是多了一个code字段，而上面是少，所以这里好处理，删了就行
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label="验证码",
                                 error_messages={  # write_only=True,序列化时不会有这个字段，不这样会报错
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },  # 错误提示自定义
                                 help_text="验证码")  # 这是一个多余的字段，不会保存到数据库中
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    # 参见DRF官方文档查看Validator的使用，验证username是否唯一
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )  # write_only=True后，这样password就不会返回了；style={'input_type': 'password'}后，DRF接口调试也是密文了

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by(
            "-add_time")  # 先查询验证码，self.initial_data里面放的是前端传过来的值
        if verify_records:
            last_record = verify_records[0]

            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):  # 这个作用于所有的字段；attrs是validate_code后的dict
        """
        重载以用来解决code多余和mobile未填写的问题
        """
        attrs["mobile"] = attrs["username"]  # 前端的手机号输入框实际是username，没有这个的话，在执行is_valid的时候会抛异常
        del attrs["code"]
        return attrs

    class Meta:
        model = User  # username是必填字段，因为User继承了django的AbstractUser类
        fields = ("username", "code", "mobile", "password")  # code本事不是User的字段，所以自己添加了code
        # 比较好的办法是前端提供username和mobile两个的input框，都post过来

    def create(self, validated_data):
        """
        ModelSerializer中有save方法，会调用这个函数
        """
        user = super(UserRegSerializer, self).create(validated_data=validated_data)  # 此处的user是我们继承的AbstractUser对象
        user.set_password(validated_data["password"])  # AbstractUser所继承的类中有一个方法叫做set_password
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    class Meta:
        model = User
        fields = ("username", "gender", "birthday", "email", "mobile")
