#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/1/29 12:34
'''
import re

from common import csv_util
from common.csv_util import ENCODING_GBK


def trim_region(region):
    if '（' in region:
        strip_index = region.index('（')
        region = region[:strip_index + 1]
    if '(' in region:
        strip_index = region.index('(')
        region = region[:strip_index + 1]

    if is_region_error_format(region):
        return None
    return region


def extra_region():
    # 2.读csv示例
    i = 0
    data = csv_util.read_csv2array("bjshhshenzhenhangzhou.csv", encoding=ENCODING_GBK)
    array = []
    error_array = []
    for index, item in enumerate(data):
        region = item['小区']
        # region = trim_region(region)
        if region:
            address = {}
            address['departmentId'] = index
            address['city'] = item['城市']
            address['region'] = item['区域']
            address['department'] = item['小区']
            roadStr = item['道路号']
            if roadStr:
                index = roadStr.index(")")
                roadStr = str.strip(roadStr[index + 1:]).replace('，', ',')
                address['road'] = roadStr
            else:
                address['road'] = ''
            if not has_error(region):
                array.append(address)
                i = i + 1
                print(f"【main({i}).road={address['city']}.{region}】")
            else:
                error_array.append(address)

    path = 'dict_department_region.csv'
    keys = csv_util.get_head_from_arr(array)
    print(f"【main().keys={keys}】")
    csv_util.create_csv(path, keys, force=True)
    csv_util.append_csv(path, array)

    path = 'dict_department_region_error.csv'
    keys = csv_util.get_head_from_arr(error_array)
    print(f"【main().keys={keys}】")
    csv_util.create_csv(path, keys, force=True)
    csv_util.append_csv(path, error_array)


def extra_road():
    # 2.读csv示例
    i = 0
    data = csv_util.read_csv2array("bjshhshenzhenhangzhou.csv", encoding=ENCODING_GBK)
    array = []
    for index_position, item in enumerate(data):
        road = item['道路号']
        if road:
            if "?" in road:
                # print(f"{i}【main().road={item}】")
                continue

            index = road.index(")")
            roadStr = str.strip(road[index + 1:]).replace('，', ',')
            split = [roadStr]
            if ',' in roadStr:
                split = roadStr.split(",")
            elif '；' in roadStr:
                split = roadStr.split("；")
                # print(f"【main(分号分割).roadStr={roadStr}】")
            for split_item in split:
                strip = str.strip(split_item)
                # strip = str.strip(split_item).replace('（', '').replace('）', '') \
                #     .replace('(', '').replace(')', '')
                road_strip = strip.strip()
                if road_strip:
                    if len(road_strip) > 0 and ('(' in road_strip or '（' in road_strip):
                        i = i + 1
                        address = {}
                        address['id'] = index_position
                        address['road'] = road_strip
                        address['department'] = road_strip
                        array.append(address)
                        print(f"【is_error_format({i}).road={road_strip}】")
                    # road_strip = trim_road(road_strip)
                    # if is_error_format(road_strip):
                    #     # i = i + 1
                    #     # print(f"【is_error_format({i}).road={road_strip}】")
                    #     continue
                    # road_strip = road_strip.replace('（', '').replace('）', '') \
                    #     .replace('(', '').replace(')', '')
                    if is_road_type(road_strip):
                        # if '上海' in item['城市']:
                        if len(road_strip) < 11:
                            address = {}
                            # address['id'] = index_position
                            # address['city'] = item['城市']
                            # address['region'] = item['区域']
                            # address['road'] = road_strip
                            # address['department'] = item['小区']
                            # array.append(address)
                            # i = i + 1
                            # print(f"【main({i}).road={address['city']}.{road_strip}】")
                    else:
                        # i = i + 1
                        # print(f"【main({i}).road={road_strip}】")
                        pass
        else:
            pass
            # print(f"没有道路号的小区【{index}.{item}】")

    # 1.写csv示例
    # array = [{'name': '小红', 'sex': 12}, {'name': '小王', 'sex': 112}]
    path = 'dict_department_road_street.csv'
    # path = 'dict_department_region.csv'
    keys = csv_util.get_head_from_arr(array)
    print(f"【main().keys={keys}】")
    csv_util.create_csv(path, keys, force=True)
    csv_util.append_csv(path, array)


def trim_road(road_strip):
    if '路' in road_strip and '弄' in road_strip:
        strip_index = road_strip.index('弄')
        road_strip = road_strip[:strip_index + 1]
    if '街' in road_strip and '弄' in road_strip:
        strip_index = road_strip.index('弄')
        road_strip = road_strip[:strip_index + 1]
    if '道' in road_strip and '弄' in road_strip:
        strip_index = road_strip.index('弄')
        road_strip = road_strip[:strip_index + 1]
    if '路' in road_strip and '号' in road_strip:
        strip_index = road_strip.index('号')
        road_strip = road_strip[:strip_index + 1]
    if '巷' in road_strip and '弄' in road_strip:
        strip_index = road_strip.index('弄')
        road_strip = road_strip[:strip_index + 1]
    if '弄' in road_strip and '号' in road_strip:
        strip_index = road_strip.index('弄')
        digtor = road_strip[strip_index - 1:strip_index]
        # print(digtor)
        if digtor and digtor.isnumeric():
            road_strip = road_strip[:strip_index + 1]
    if '弄' in road_strip and '支弄' in road_strip:
        strip_index = road_strip.index('弄')
        digtor = road_strip[strip_index - 1:strip_index]
        # print(digtor)
        if digtor and digtor.isnumeric():
            road_strip = road_strip[:strip_index + 1]
    #             # print(strip)
    #             # print(road_strip)
    if '街' in road_strip and '号' in road_strip:
        strip_index = road_strip.index('号')
        road_strip = road_strip[:strip_index + 1]
        # i = i + 1
        # print(f"【extra_road({i}).街 ,号={strip}==={road_strip}】")
    if '道' in road_strip and '号' in road_strip:
        strip_index = road_strip.index('号')
        road_strip = road_strip[:strip_index + 1]
    if '巷' in road_strip and '号' in road_strip:
        strip_index = road_strip.index('号')
        road_strip = road_strip[:strip_index + 1]
    if '号院' in road_strip:
        strip_index = road_strip.index('院')
        road_strip = road_strip[:strip_index + 1]
        # print(f"【extra_road().号院={strip}==={road_strip}】")
    if '省' in road_strip:
        strip_index = road_strip.index('省')
        road_strip = road_strip[strip_index + 1:]
        # print(f"【extra_road().县={strip}==={road_strip}】")
    if '市' in road_strip:
        strip_index = road_strip.index('市')
        road_strip = road_strip[strip_index + 1:]
    if '县' in road_strip:
        strip_index = road_strip.index('县')
        road_strip = road_strip[strip_index + 1:]
    if '区' in road_strip:
        strip_index = road_strip.index('区')
        road_strip = road_strip[strip_index + 1:]
        # i = i + 1
        # print(f"【main({i}).road={strip}==={road_strip}】")
    return road_strip


def is_error_format(road_strip):
    if '.' in road_strip or '-' in road_strip or '/' in road_strip or '、' in road_strip:
        return True
    if '~' in road_strip:
        return True
    if '?' in road_strip:
        return True
    if '与' in road_strip:
        return True
    if not re.search(r'\d', road_strip):
        return True
    if '（' in road_strip or '(' in road_strip:
        return True
    return False


def is_region_error_format(road_strip):
    if '.' in road_strip or '-' in road_strip or '/' in road_strip or '、' in road_strip:
        return True
    if '~' in road_strip:
        return True
    if '?' in road_strip:
        return True
    if '（' in road_strip or '(' in road_strip:
        return True
    return False


def is_road_type(road_strip):
    return '路' in road_strip and '号' in road_strip or \
           '弄' in road_strip or \
           '院' in road_strip or \
           '道' in road_strip and '号' in road_strip or \
           '里' in road_strip and '号' in road_strip or \
           '巷' in road_strip and '号' in road_strip or \
           '同' in road_strip and '号' in road_strip or \
           '区' in road_strip and '号' in road_strip or \
           '营' in road_strip and '号' in road_strip or \
           '庄' in road_strip and '号' in road_strip or \
           '园' in road_strip and '号' in road_strip or \
           '场' in road_strip and '号' in road_strip or \
           '浜' in road_strip and '号' in road_strip
    # '街' in road_strip or \
    # '号' in road_strip or \
    # '村' in road_strip and '号' in road_strip or \


def has_error(road_strip):
    return '?' in road_strip


def is_region_type(road_strip):
    return not ('路' in road_strip and '号' in road_strip or \
                '弄' in road_strip or \
                '院' in road_strip or \
                '道' in road_strip and '号' in road_strip or \
                '里' in road_strip and '号' in road_strip or \
                '巷' in road_strip and '号' in road_strip or \
                '同' in road_strip and '号' in road_strip or \
                '区' in road_strip and '号' in road_strip or \
                '营' in road_strip and '号' in road_strip or \
                '庄' in road_strip and '号' in road_strip or \
                '园' in road_strip and '号' in road_strip or \
                '场' in road_strip and '号' in road_strip or \
                '浜' in road_strip and '号' in road_strip or \
                '街' in road_strip or \
                '号' in road_strip or \
                '村' in road_strip and '号' in road_strip)


if __name__ == '__main__':
    extra_region()
    # extra_road()
