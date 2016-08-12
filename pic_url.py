# -*- coding:utf-8 -*-

import os
import sys
import cgitb
import urlparse
import time
import requests
import json
import MySQLdb
import urllib2
import hashlib
from wechat_sdk import WechatBasic
import sys

reload(sys)
sys.setdefaultencoding('utf8')


requests=requests.Session()

def get_zhihudaily():
    headers = {
        'User-Agent': 'Mozilla / 5.0(X11;Linuxx86_64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 50.0.2661.102Safari / 537.36'
    }
#    json_str_data = requests.get('http://www.zhihu.com',headers=headers)
    json_str_data = requests.get('http://news-at.zhihu.com/api/4/news/latest',headers=headers)
#    print json_str_data.content
    json_data = json.loads(json_str_data.content)['stories']
    news_str = []

    count = 0
    for x in json_data:

        news_str.append({'title': x["title"], 'url': 'http://daily.zhihu.com/story/' + str(x['id']), 'picurl': x["images"][0].replace('\\/', '/')})
        count += 1

        if count == 10:
            break
        print news_str[0]["title"]
    return news_str


print get_zhihudaily()
