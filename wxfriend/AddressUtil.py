#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/12/9 18:39
'''
import json
import os

import cpca
import numpy as np
import requests
from LAC import LAC

from common import Logger, csv_util, time_util
from common.csv_util import read_csv2array


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
    lac.load_customization('./LacModels/custom.csv', sep=None)
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
        if ('m' == type or '弄' == item[0][index]) and (
                index <= location_index + 3) and location_index > -1:
            location.append(item[0][index])
    return location


def put_addresss(item):
    '''
    上传图片ids
    :param md5:
    :param file_ids:
    :return:
    '''
    Logger.println(f"【put_addresss().item={item}】")
    try:
        res = requests.put("http://internal.zuker.im/moment",
                           json=item)
        res_json = res.json()
        jsonstr = json.dumps(res_json, indent=4, ensure_ascii=False)
        Logger.println(f"put_addresss【res={jsonstr}】")
        if res_json['code'] == 0:
            return True
        else:
            return False
    except Exception as e:
        Logger.println(f"Exception is【{e}】")
        return False


page = 1


def batch_recongnize():
    global page
    index_position = 0
    totalpage = 1
    location_arr = []
    md5_contents = []
    while True:
        if page > totalpage:
            break
        totalpage, items = get_moment_by_page(page)
        print(f"【page={page}】")
        print(f"【totalpage={totalpage}】")
        if items and totalpage > 0:
            for item in items:
                location_str = item['content'].replace('\n', '').replace('\r', '')
                print(f"【location_str.{index_position}={location_str}】")
                index_position += 1
                location_arr.append(location_str)
                md5_contents.append(item['content_md5'])
            page += 1
    addresss = get_address_by_custom_lac(location_arr)
    address_arr = []
    for index, item in enumerate(addresss):
        loc_from = getLocFrom(item)
        if loc_from:
            print(f"【文本内容:{location_arr[index]}】")
            print(f"【检测到地址:{loc_from}】")
            print(f"【检测到地址:{'/'.join(loc_from)}】")
            item = {}
            item['md5_content'] = md5_contents[index]
            item['address'] = '/'.join(loc_from)
            address_arr.append(item)
            path = f"address_{time_util.now_to_date('%Y-%m-%d')}.csv"
            keys = csv_util.get_head_from_arr(address_arr)
            if not os.path.exists(path):
                csv_util.create_csv(path, keys)
            csv_util.append_csv(path, address_arr)
            # b = put_addresss(item)
            # print(f"【存储地址信息:{item},存储结果={b}】")


if __name__ == '__main__':
    data = read_csv2array("dict_department_simple.csv")
    location_arr = [item['department'] for item in data]
    addresss = get_address_by_custom_lac(location_arr)
    address_arr = [getLocFrom(item) for item in addresss]
    for index, item in enumerate(address_arr):
        print(f"【().{index}.{item}】")
