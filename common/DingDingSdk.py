#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/2/21 上午10:59
# @Author  : 张新礼
# @File    : 钉钉自动发消息.py
# @Software: PyCharm
import json
import requests

debug = False


def send_message(msg):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=4f2018d9200e29610e4c55fbacd13e290d061345084dd6899384ff7d6d178f65'
    pagrem = {
        "msgtype": "text",
        "text": {
            "content": "%s" % (msg)
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    if not debug:
        requests.post(url, data=json.dumps(pagrem), headers=headers)


if __name__ == "__main__":
    send_message('朋友圈:测试通知!')
