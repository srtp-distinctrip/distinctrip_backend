"""distinctrip_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
import xadmin
from distinctrip_backend.settings import MEDIA_ROOT
from django.views.static import serve  # 这是django专门来做静态文件view的serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from scenic.views import ScenicViewSet
from article.views import ArticleViewSet
from users.views import SmsCodeViewSet, UserViewSet
from operation.views import UserFavViewSet, LeavingMessageViewSet, QuestionnaireViewSet, RouteViewSet


router = DefaultRouter()

# 配置goods的url
router.register(r'scenic', ScenicViewSet, base_name="scenic")
# 配置article的url
router.register(r'article', ArticleViewSet, base_name="article")
# 配置code的url
router.register(r'code', SmsCodeViewSet, base_name="code")
# 配置user的url
router.register(r'users', UserViewSet, base_name="users")
# 配置userfav的url
router.register(r'userfavs', UserFavViewSet, base_name="userfavs")
# 配置message的url
router.register(r'messages', LeavingMessageViewSet, base_name="messages")
# questionnaire
router.register(r'questionnaire', QuestionnaireViewSet, base_name="questionnaire")
# route
router.register(r'route', RouteViewSet, base_name="route")

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'docs/', include_docs_urls(title="Distinctrip后端接口文档")),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api-token-auth/', obtain_jwt_token),
]
