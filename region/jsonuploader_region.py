#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/1/27 16:33
'''
import json
import time

import requests

from common.csv_util import read_csv2array

ONLINE_URL = 'http://47.104.145.32:9111/letter-data-center/api/v1/es_department'
OFFLINE_URL = 'http://47.104.193.230:9500/api/v1/es_department'


def getUploadUrl():
    return ONLINE_URL if online else OFFLINE_URL


def getBatchUploadUrl():
    url = f'{ONLINE_URL if online else OFFLINE_URL}/batch'
    print(f"【getBatchUploadUrl().url={url}】")
    return url


def upload(array):
    for index, item in enumerate(array):
        time.sleep(1)
        address = {
            "departmentId": str(item['departmentId']),
            "department": item['department'],
            "city": item['city'],
            "region": item['region'],
            "road": item['road']
        }
        print(f"开始上传数据【({index}).item={address}】")
        res = requests.post(getUploadUrl(), json=address)
        res_json = res.json()
        jsonstr = json.dumps(res_json, indent=4, ensure_ascii=False)
        print(f"【上传结果({index}).{address}.res={jsonstr}】")


def upload_batch(array):
    des_arr = []
    for index, item in enumerate(array):
        address = {
            "departmentId": item['departmentId'],
            "department": item['department'],
            "city": item['city'],
            "region": item['region'],
            "road": item['road']
        }
        des_arr.append(address)
    print(f"即将上传数据【{len(des_arr)}条】")
    res = requests.post(getBatchUploadUrl(), json=des_arr)
    res_json = res.json()
    jsonstr = json.dumps(res_json, indent=4, ensure_ascii=False)
    print(f"【上传结果res={jsonstr}】")


# 线上线下开关
online = True

if __name__ == '__main__':
    arr = read_csv2array("2021-02-08_dict_department_region_all.csv")
    upload_batch(arr)
