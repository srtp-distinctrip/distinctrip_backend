__author__ = 'dmxjhg'
__date__ = '2019/8/13 19:50'

from rest_framework import serializers

from .models import Scenic, ScenicImage


class ScenicImageSerializer(serializers.ModelSerializer):
    """
    商品图片序列化
    """
    class Meta:
        model = ScenicImage
        fields = ("image", )


class ScenicSerializer(serializers.ModelSerializer):
    """
    对商品数据序列化
    """
    images = ScenicImageSerializer(many=True)  # 在商品信息所拥有的字段的基础上多了images，不同于外键，这本身不是Goods的属性

    class Meta:
        model = Scenic
        fields = "__all__"
