#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/2/7 17:41
'''
import json

import requests

from common import Logger, csv_util, time_util, re_util, poisearch
from common.csv_util import read_csv2array
from region.city_code_transfer import has_citycode, get_citycode

pageSize = 2000


def get_region_by_page(page):
    item = {"page": page, "page_size": pageSize}
    res = requests.get("http://internal.zuker.im/department", params=item)
    res_json = res.json()
    if res_json['code'] == 0:
        total_page = res_json['result']['total_page']
        items = res_json['result']['items']
        return total_page, items
    else:
        Logger.println(f"【接口异常】{res_json}")
        return None


page = 1


def batch_recongnize():
    global page
    index_position = 0
    totalpage = 1
    region_arr = []
    while True:
        if page > totalpage:
            break
        totalpage, items = get_region_by_page(page)
        print(f"【page={page}】")
        print(f"【totalpage={totalpage}】")
        page += 1
        if items and totalpage > 0:
            for item in items:
                address = {
                    "departmentId": str(item['department_id']),
                    "city": item['city'],
                    "region": item['region'],
                    "department": item['title'],
                    "road": item['road']
                }
                region_arr.append(address)
                index_position += 1
                region_str = item['title']
                print(f"【location_str.{index_position}={region_str}】")

    path = f'{time_util.now_to_date("%Y-%m-%d")}_dict_department_region_all.csv'
    keys = csv_util.get_head_from_arr(region_arr)
    csv_util.create_csv(path, keys, force=True)
    csv_util.append_csv(path, region_arr)


def get_jsonfrom_file(name):
    with open(name, 'r', encoding='utf-8') as load_f:
        load_dict = json.load(load_f)
    return load_dict


def extra_region(arr):
    regions = []
    citys = []
    for index, region in enumerate(arr):
        address = f"{region['city']}|{region['region']}"
        regions.append(address)
    regions_norepeat = list(set(regions))
    # dumps = json.dumps(regions_norepeat, indent=4, ensure_ascii=False)
    # print(f"【extra_region({len(regions_norepeat)}条).regions_norepeat={dumps}】")
    return regions_norepeat


if __name__ == '__main__':
    count = 0
    # batch_recongnize()
    arr = read_csv2array("2021-02-08_dict_department_region_all.csv")
    region_arr = []
    for item in arr:
        if '上海' in item['city'] and not "上海周边" in item['region']:
            region_arr.append(item)
            count = count + 1
    print(f"【().count={count}】")
    path = f'{time_util.now_to_date("%Y-%m-%d")}_dict_department_shanghai.csv'
    keys = csv_util.get_head_from_arr(region_arr)
    csv_util.create_csv(path, keys, force=True)
    csv_util.append_csv(path, region_arr)
