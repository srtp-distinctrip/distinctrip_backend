__author__ = 'dmxjhg'
__date__ = '2019/8/14 18:34'

import json
import requests
from distinctrip_backend.settings import APIKEY


class YunPian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        parmas = {
            "apikey": self.api_key,
            "mobile": mobile,
            # text的格式必须是模板格式（如果有），并对变量code进行替换
            "text": "【刘家豪】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }

        response = requests.post(self.single_send_url, data=parmas)  # 返回response.text的实际上是字符串
        re_dict = json.loads(response.text)  # 所以需要解析response.text
        return re_dict


if __name__ == "__main__":
    """
    用来测试发送功能，当DRF提供了相应的接口后，可以注释掉
    """
    yun_pian = YunPian(APIKEY)
    yun_pian.send_sms("3265", "13076097216")
