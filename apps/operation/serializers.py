__author__ = 'dmxjhg'
__date__ = '2019/8/13 19:50'

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav, Questionnaire, Route
from .models import UserLeavingMessage

from article.serializers import ArticleSerializer


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )  # 获取当前用户，drf文档中看用法，如果不这样，post的时候还需要传用户，这是不合理的

    class Meta:
        model = UserFav
        fields = ("user", "article", "id")  # id是为了删除操作
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'article'),
                message="已经收藏"
            )
        ]


class UserFavDetailSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()

    class Meta:
        model = UserFav
        fields = ("article", "id")


class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message", "add_time")


class QuestionnaireSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = Questionnaire
        fields = ("user", "choose", "add_time", "id")


class RouteListSerializer(serializers.ModelSerializer):
    questionnaire = QuestionnaireSerializer()
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    route = serializers.CharField(read_only=True, )

    class Meta:
        model = Route
        fields = ("user", "questionnaire", "route", "add_time")
