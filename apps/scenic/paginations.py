from rest_framework.pagination import PageNumberPagination


class ScenicPagination(PageNumberPagination):
    """
    分页相关配置
    """
    # 每页默认展示数据的数量
    page_size = 12
    # url中的 ?page=3 中的page就是由此字段决定的
    page_query_param = "page"
    # 在url后加 ?page_size=20 ，则每页展示20条数据，实现前端动态配置
    page_size_query_param = 'page_size'
    # 每页展示的数据条数的最大值
    max_page_size = 100
