#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/1/27 16:33
'''
import json

import requests

from common.csv_util import read_csv2array


def search(region='上海', query=None):
    param = {}
    param['query'] = query
    param['tag'] = '小区,道路号'
    param['region'] = region
    param['output'] = 'json'
    param['city_limit'] = True
    param['ak'] = 'GOqvzedjVuNXBG8D0POc2smt'
    res = requests.get("http://api.map.baidu.com/place/v2/search", params=param)
    url = res.url
    print(f"【search().url={url}】")
    json = res.json()
    if json:
        results_ = json.get('results')
        if results_:
            print(f"【search().搜索的地址={query}】")
            print(f"【search().搜索的地址类别={param['tag']}】")
            if results_:
                for item in results_:
                    result0 = item['address']
                    print(f"【search({query}).关联地址={result0}】")
        else:
            print(f"【search({query}).无关联地址】")
    else:
        print(f"【search({query}).无关联地址】")


if __name__ == '__main__':
    arr = read_csv2array("dict_department_region.csv")
    for index, item in enumerate(arr):
        department_ = item['department']
        city = item['city']
        print(f"【{index}.item={item}】")
        search(city,department_)
