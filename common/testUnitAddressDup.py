#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/7/23 14:45
'''
import requests

from common import poisearch, LogUtil, Bd2Gaode

def getLonLat(city, department):
    search = poisearch.search(city, department)
    if search:
        search_ = search[0]
        print(f"【getLonLat().search={search_}】")
        return search_["location"], search_['area']
    return None

def  checkAddressName(address):
    city = address['city']
    department = address['department']
    road = address['road']
    street = address['street']
    lat, region = getLonLat(city, department)
    lng, lat = Bd2Gaode.bdToGaoDe(float(lat['lng']), float(lat['lat']))
    url = f"http://services.api.zuker.im/agent/v3/house/4b375c16eb8cab0d219caf52/dup?" \
          f"city={city}" \
          f"&region={region}" \
          f"&department={department}" \
          f"&road={road}" \
          f"&street={street}" \
          f"&longitude={lng}&latitude={lat}"
    print(f"【url().lng={url}】")
    res = requests.get(url)
    url = res.url
    jsonstr = res.json()['result']['items']
    size = len(jsonstr)
    print(f"【().相似房源数量为={size}】")
    if size > 0:
        for item in jsonstr:
            house_ = item['house']
            print(f"【().format_address_title={house_['format_address_title']}】")

if __name__ == '__main__':
    address = {
        "city": '上海',
        "department": '华联创意广场',
        "road": '江苏北路1205',
        "street": '北屋'}
    checkAddressName(address)

