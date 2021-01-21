#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/12/9 18:39
'''

import cpca
import numpy as np
import requests
from LAC import LAC

from common import Logger


def stand_recongnize_address(location_str):
    global pd
    pd = cpca.transform(location_str, pos_sensitive=True)
    keys = list(pd)
    np_array = np.array(pd)
    datas = []
    for array in np_array:
        data = {}
        for index in range(len(keys)):
            if array[index]:
                data[keys[index]] = array[index]
        if data:
            datas.append(data)
    return datas


def get_moment_by_page(page):
    item = {"page": page}
    res = requests.get("http://internal.zuker.im/moment/list", params=item)
    res_json = res.json()
    if res_json['code'] == 0:
        total_page = res_json['result']['total_page']
        items = res_json['result']['items']
        return total_page, items
    else:
        Logger.println(f"【接口异常】{res_json}")
        return None


def get_address_by_lac(texts):
    # 装载分词模型
    lac = LAC(mode='lac')
    # 单个样本输入，输入为Unicode编码的字符串
    seg_result = lac.run(texts)
    return seg_result

def get_address_by_custom_lac(texts):
    lac = LAC()
    lac.load_customization('./LacModels/custom.tsv', sep=None)
    # 干预后结果
    custom_result = lac.run(texts)
    return custom_result

def getLocFrom(item):
    location = []
    location_index = -1
    for index, type in enumerate(item[1]):
        if 'LOC' == type:
            location.append(item[0][index])
            location_index = index
        if ('m' == type or '弄' ==item[0][index]) and (index <= location_index + 3) and location_index > -1:
            location.append(item[0][index])
    return location



page = 1
if __name__ == '__main__':
    totalpage, items = get_moment_by_page(page)
    location_arr = []
    for item in items:
        location_str = item['content'].replace('\n', '').replace('\r', '')
        # print(f"【().location_str={location_str}】")
        location_arr.append(location_str)
    addresss = get_address_by_custom_lac(location_arr)
    for index, item in enumerate(addresss):
        # print(f"【().item={item}】")
        loc_from = getLocFrom(item)
        if loc_from:
            print(f"【文本内容:{location_arr[index]}】")
            print(f"【检测到地址:{loc_from}】")
            print(f"【检测到地址:{'/'.join(loc_from)}】")
            print(f"【中文:{item[0]}】")
            print(f"【词性:{item[1]}】")
