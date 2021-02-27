#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/2/10 14:47
'''
import json


def get_jsonfrom_file(name):
    with open(name, 'r', encoding='utf-8') as load_f:
        load_dict = json.load(load_f)
    return load_dict


def get_all_region():
    files = get_jsonfrom_file("./data/area.json")
    result_ = files['result']
    all_regions = []
    for item in result_:
        region = {}
        region['id'] = item['id']
        region['parent_id'] = item['parent_id']
        region['name'] = item['name']
        all_regions.append(region)
    return all_regions


def has_citycode(city,region):
    citycode=-1
    citycode_item = get_citycode(city)
    if citycode_item:
        citycode=  citycode_item["id"]
    all_region = get_all_region()
    if all_region:
        for item in all_region:
            if region+"区" == item['name']  or region == item['name'] or region+"新区" == item['name']:
                return True
    return False

def get_citycode(region):
    all_region = get_all_region()
    if all_region:
        for item in all_region:
            if region in item['name']:
                return item
    return None


if __name__ == '__main__':
    citycode = has_citycode('长宁区')
    print(f"【().has_citycode()={citycode}】")
