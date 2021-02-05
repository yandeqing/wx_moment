#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/1/27 16:33
'''
import json

import requests

from common.csv_util import read_csv2array


def upload(array):
    for index, item in enumerate(array):
        address = {
            "address": item['department'],
            "city": item['city'],
            "region": item['region'] + '区',
            "type": 2
        }
        # print(f"开始上传数据【({index}).item={address}】")
        res = requests.post("http://47.104.193.230:9500/api/v1/es_address", json=address)
        res_json = res.json()
        jsonstr = json.dumps(res_json, indent=4, ensure_ascii=False)
        print(f"【上传结果({index}).{address}.res={jsonstr}】")


if __name__ == '__main__':
    arr = read_csv2array("dict_department_region.csv")
    upload(arr)
