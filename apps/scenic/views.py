from rest_framework import viewsets
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response

from .filters import ScenicFilter
from .paginations import ScenicPagination
from .models import Scenic
from .serializers import ScenicSerializer


class ScenicViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """
    list:
        商品列表页展示（分页，过滤，搜索，排序）
    retrieve:
        商品详情页展示
    """
    queryset = Scenic.objects.all().order_by("add_time")
    serializer_class = ScenicSerializer

    pagination_class = ScenicPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = ScenicFilter
    search_fields = ('name', 'scenic_brief', 'scenic_desc')
    ordering_fields = ('click_num', 'visit_num', 'fav_num', 'price')

    def retrieve(self, request, *args, **kwargs):
        """
        商品详情页展示，重载了retrieve方法，在展示详情的时候，点击量 +1
        """
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
