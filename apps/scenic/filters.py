import django_filters

from .models import Scenic


class ScenicFilter(django_filters.rest_framework.FilterSet):
    """
    景点过滤定制类
    """
    click_num = django_filters.NumberFilter(field_name='click_num', help_text="最低点击量", lookup_expr='gte')
    city = django_filters.CharFilter(field_name='province', lookup_expr='icontains')
    province = django_filters.CharFilter(field_name='province', lookup_expr='icontains')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    lable = django_filters.CharFilter(field_name='lable', lookup_expr='icontains')

    class Meta:
        model = Scenic
        fields = ['click_num', 'city', 'province', 'name', 'lable']
