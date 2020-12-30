#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/2/21 上午10:59
# @Author  : 张新礼
# @File    : 钉钉自动发消息.py
# @Software: PyCharm
import json
import requests


def send_message(msg):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=befbb4bf901cfb57ae7906381c7b4219ceebc8172d545347d83ede8d174e32dd'
    pagrem = {
        "msgtype": "text",
        "text": {
            "content": "朋友圈：%s " % (msg)
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    requests.post(url, data=json.dumps(pagrem), headers=headers)


if __name__ == "__main__":
    send_message('hello world!')
