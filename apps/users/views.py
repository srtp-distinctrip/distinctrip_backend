from random import choice

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


from .models import VerifyCode
from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from utils.verify_code import YunPian
from distinctrip_backend.settings import APIKEY

User = get_user_model()

# Create your views here.


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    继承这个类，然后重写authenticate方法
    """
    def authenticate(self, username=None, password=None, **kwargs):  # 然后重写这个函数
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))  # 查询用户方式增加了mobile，原本只有username
            if user.check_password(password):  # 仍然是通过password验证用户，check_password会对传过来的password（名文）进行加密，然后比对
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码
        """
        seeds = "1234567890"  # 种子
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)  # 原本是一个数组

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # 拿到上边的serializer
        serializer.is_valid(raise_exception=True)  # 这里如果=True，这一步如果出错，直接抛异常，不会进入下面的代码行；这里is_valid出错，返回400

        mobile = serializer.validated_data["mobile"]  # 上面已经验证了，能跑到这一步，所以mobile一定是有的
        yun_pian = YunPian(APIKEY)
        code = self.generate_code()
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)  # 返回的是re_dict，可以点进去看看
        # 下面来解析这个变量
        if sms_status["code"] != 0:  # 返回的status代表的含义可以看一看云片网的文档
            return Response({
                "mobile": sms_status["msg"]  # msg中放的是云片网错误信息
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)  # 成功后返回的是手机号


class UserViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserDetailSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

    def create(self, request, *args, **kwargs):
        """
        重载create方法，在注册时调用
        重载的目的是向前端返回token，实现注册后自动登录
        """
        serializer = self.get_serializer(data=request.data)  # 这里没变，获取用来做有效性验证、序列化的serializer实例
        serializer.is_valid(raise_exception=True)  # 这里没变，验证上面的实例是否有效，如果检测出异常，则直接抛出而不会再执行下面的代码，异常的status为400
        user = self.perform_create(serializer)  # 这里变了，拿到user（perform_create是被重载了的），这个user就是UserProfile对象
        # 下面4行是新增的代码
        re_dict = serializer.data  # 相当于re_dict复制了Response中原本要return的的参数serializer.data，返回时返回re_dict就好
        payload = jwt_payload_handler(user)  # 生成payload，这个逻辑可以从url接口处的view开始跟踪，能够找到
        re_dict["token"] = jwt_encode_handler(payload)  # 生成token，这个逻辑可以从url接口处的view开始跟踪，能够找到，并将其放进re_dict
        re_dict["username"] = user.username  # 这是新加的，将name也添加进响应中，添加token和name是因为前端需要
        # 上面4行是新增的代码
        headers = self.get_success_headers(serializer.data)  # 这里没变，是响应的header信息
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)  # 这里的响应对象将serializer.data换成了re_dict

    def perform_create(self, serializer):
        """
        重载了这个函数，点进去看看原函数，它只是调用了save方法，并没有进行返回
        我们重载它，在保存的同时返回它
        """
        return serializer.save()  # 保存并返回UserProfile对象（保存和返回的对象决定于serializer类中的meta配置）

    def get_object(self):
        return self.request.user
