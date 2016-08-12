#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import os
import sys
import cgitb
import urlparse
import time
import requests
import json
import MySQLdb
import hashlib
import chardet
from wechat_sdk import WechatBasic
neirong = u'qlzx'


post_form=u'''
<xml>
 <ToUserName><![CDATA[Daniel_dev]]></ToUserName>
 <FromUserName><![CDATA[oITgtv_3lUawCfSA3XcYjv_xAgWs]]></FromUserName>
 <CreateTime>1464678350</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[%s]]></Content>
 <MsgId>1234567890123458</MsgId>
 </xml>''' %neirong
headers={'User-Agent':"Mozilla/4.0"}
r=requests.Session()
#个人
#APPID="wx2e8e5b1b8ac4a483"
#SECRET="8bbfede36e21f23bc4533893d130e471"

#测试
APPID="wx35ce6a5beb19277e"
SECRET="3T2kNFae1eb7cxuKzlliWp3GvHh-AbI545dYYGsfbN9L3jwhPdNkQNxaSXUjf0c5"


timestamp=str(int(time.time()))
nonce="1923162992"

#知乎专栏
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
    news_str1=json.dumps(news_str)
    return news_str

def get_token():
    url_b = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    url = url_b +"?"+"corpid"+"="+APPID+"&"+"corpsecret="+SECRET
    cc=r.get(url)
    dd=json.loads(cc.content)
    print dd
    return  dd["access_token"]

def get_userid():
    ACCESS_TOKEN=get_token()
    print ACCESS_TOKEN
#    url="https://api.weixin.qq.com/cgi-bin/user/get?access_token="+ACCESS_TOKEN+"&next_openid="
    url = "https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token=s7B4q-q_H0l1g1QgQmGxoJl6w6vVDYbj7POWES-ZDgrpAmrF_gd-F9sKm9N_CWJy&userid=yinting"
    user=r.get(url)
    print type(user)
    return json.loads(user.content)

def send_message(data):
    data=data
    headers = {
        'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'Accept-Encoding': "gzip, deflate",
        'Cache-Control': "max-age=0",
        'Connection': "keep-alive",
        'Content-Length': "90",
        'Upgrade-Insecure-Requests':"1",
        'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
    }
    template = {
        "touser": "",
        "toparty": "",
        "totag": "",
        "msgtype": "text",
        "agentid": "",
        "text": {
            "content": ""
        },
        "safe": "0"
    }
    template['touser'] = "longbo"
    template['agentid'] = 2
    template['text']['content'] = data
    print data
    content = json.dumps(template, ensure_ascii=False)
    print content
    ACCESS_TOKEN = get_token()

    url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="+ACCESS_TOKEN
    b= r.post(url,data=content)
    print b.content

def send_news(data):
    data=data
    headers = {
        'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'Accept-Encoding': "gzip, deflate",
        'Cache-Control': "max-age=0",
        'Connection': "keep-alive",
        'Content-Length': "90",
        'Upgrade-Insecure-Requests':"1",
        'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
    }
    template = {
        "touser": "",
        "toparty": "",
        "totag": "",
        "agentid": "",
        "msgtype": "news",
        "news":{
        "articles":[
            {"title":"情人节快乐～波仔子",
             "description": "aaaa",
             "url":"http://www.bobozhu.cn/test/heart.html",
             "picurl":"http://www.bobozhu.cn/test/11111.jpg"
            },
            {"title": "",
             "description": "aaaa",
             "url": "",
             "picurl": ""
             }
        ]
        }
    }
    template['touser'] = "qujun|longbo"
    template['agentid'] = 2
    print data
#    template['news']['articles'][0]['url']=data[0]['url']
#    template['news']['articles'][0]['picurl']=data[0]['picurl'].encode('utf8')
#    template['news']['articles'][0]['title'] = data[0]['title'].encode('utf8')
    template['news']['articles'][1]['url'] = data[3]['url']
    template['news']['articles'][1]['title'] = data[3]['title'].encode('utf8')
    template['news']['articles'][1]['picurl'] = data[3]['picurl'].encode('utf8')
#    print type(template['news']['articles'][0]['title'])
    content = json.dumps(template, ensure_ascii=False)
    print content
    ACCESS_TOKEN = get_token()

    url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=-QlHQ7sIjg4Ooha-GUjlYYKljp3aYr-sMDAWBfjrk4e3nDHTQXr_C_G_p2DqEpns"
    b= r.post(url,data=content)
    print b.content

def gen_sign():
    s = ["1464855898"] + ["123123"] + [nonce]
    s.sort()
    s = ''.join(s)
    return hashlib.sha1(s).hexdigest()


def auth():
    signature=gen_sign()
    url="http://114.215.159.93/?msg_signature=87e8433a5aa0c5be6002bfcb012fd235df49dbdc&timestamp=1464860366&nonce=875401665&echostr=9Gs8M1PN2Bk70l9v9%2FLCTzpRRLClBoUaqTmB%2BBxFyZFP1cFTBlFy%2FLhj0hxP8J%2B%2FFtB%2FTtn4pQg8a8QD5TljXQ%3D%3D"
    print url
#    c=r.get(url)
#    print c.content
    b=r.post(url, headers=headers,data=post_form)
    print b.content
#    print type(b.content)
#    with open("alibobo.html",'wb') as fuck:
#        fuck.write(b.content)

#print get_userid()
send_news(get_zhihudaily())
#send_message(get_zhihudaily()[0])
#auth()
#print get_zhihudaily()[0]
#print get_token()
#print gen_sign()
#auth()