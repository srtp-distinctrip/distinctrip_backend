__author__ = 'dmxjhg'
__date__ = '2019/8/14 23:34'

import requests

api= "http://api.map.baidu.com/directionlite/v1/riding"

parmas = {
    "origin": "40.01116,116.339303",
    "destination":"39.936404,116.452562",
    "ak":"0yH8jShLqhnBljfQQ5b3jkxCdDDsU8xj"
}

url = api + "?origin=" + parmas.get("origin") + "&destination=" + parmas.get("destination") + "&ak=" + parmas.get("ak")
print(url)
response = requests.get(url=url)
print(response.text)
