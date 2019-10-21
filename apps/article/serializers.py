__author__ = 'dmxjhg'
__date__ = '2019/8/13 19:50'

from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """
    路书数据序列化
    """
    class Meta:
        model = Article
        fields = "__all__"

