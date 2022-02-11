#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/1/27 16:33
'''
import json
import time

import requests

from common import csv_util, re_util, Bd2Gaode, LogUtil
from common.csv_util import read_csv2array


def search_city_regions(region='上海', query=None):
    param = {}
    param['query'] = query
    param['tag'] = '道路|小区'
    param['region'] = region
    param['output'] = 'json'
    param['city_limit'] = True
    param['ak'] = 'GOqvzedjVuNXBG8D0POc2smt'
    res = requests.get("http://api.map.baidu.com/place/v2/search", params=param)
    url = res.url
    jsonstr = res.json()
    if jsonstr:
        results_ = jsonstr.get('results')
        res = []
        if results_:
            if results_:
                return list(set([item.get('area') for item in results_]))
        else:
            pass
    else:
        pass

def search(region='上海', query=None):
    param = {}
    param['query'] = query
    param['tag'] = '道路|小区'
    param['region'] = region
    param['output'] = 'json'
    param['city_limit'] = True
    param['ak'] = 'GOqvzedjVuNXBG8D0POc2smt'
    res = requests.get("http://api.map.baidu.com/place/v2/search", params=param)
    url = res.url
    print(f"【search().url={url}】")
    jsonstr = res.json()
    if jsonstr:
        results_ = jsonstr.get('results')
        res = []
        if results_:
            print(f"【search().搜索的地址={query}】")
            if results_:
                res = "|".join([f"{item.get('name')}{item.get('address')}" for item in results_])
                dump = json.dumps(results_, indent=4, ensure_ascii=False)
                # print(f"【search().jsonstr={dump}】")
            return results_
        else:
            print(f"【search({query}).无关联地址】")
    else:
        print(f"【search({query}).无关联地址】")


if __name__ == '__main__':
    # arr = read_csv2array("dict_department_region_error.csv")
    # i = 0
    # baidu_road_arr = []
    # baidu_road_arr_error = []
    # for item in arr:
    #     time.sleep(1)
    #     address = {
    #         "departmentId": str(item['departmentId']),
    #         "city": item['city'],
    #         "region": item['region'] + '区',
    #         "department": item['department'],
    #         "road": item['road']
    #     }
    #     city = item['city']
    #     road = item['road']
    #     department_ = item['department']
    #     if department_:
    #         road_des = search(city, department_)
    #         replace = department_.replace("?", "\w?")
    #         reg_res = re_util.search_text_by_reg(replace, road_des)
    #         if reg_res:
    #             address['department'] = reg_res
    #             if "?" in road:
    #                 reg_res_road = road.replace(department_, reg_res)
    #                 if reg_res_road:
    #                     address['road'] = reg_res_road
    #                     print(f"【main({i}).reg_res_road={reg_res_road}】")
    #             i = i + 1
    #             print(f"【main({i}).road==>{address}】")
    #             baidu_road_arr.append(address)
    #         else:
    #             baidu_road_arr_error.append(address)
    #
    # path = 'dict_department_region_error_complete.csv'
    # keys = csv_util.get_head_from_arr(baidu_road_arr)
    # csv_util.create_csv(path, keys, force=True)
    # csv_util.append_csv(path, baidu_road_arr)
    #
    # path = 'dict_department_region_error_complete_not.csv'
    # keys = csv_util.get_head_from_arr(baidu_road_arr_error)
    # csv_util.create_csv(path, keys, force=True)
    # csv_util.append_csv(path, baidu_road_arr_error)
    lat = search('上海', '御翠豪庭')
    if lat:
        print(f"【().address={lat}】")
