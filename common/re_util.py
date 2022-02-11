#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/2/7 13:19
'''
import re


def search_text_by_reg(reg, text):
    try:
        search = re.search(reg, text)
        groups = search.group()
        return groups
    except:
        return None


def find_texts_by_reg(reg, text):
    try:
        searchs = re.findall(reg, text)
        return searchs
    except:
        return None


if __name__ == '__main__':
    testText = "江苏北路1弄125号A座"
    road = search_text_by_reg(r'(^[\u4e00-\u9fa5]{0,})', testText)
    if road:
        print(road)
    search = find_texts_by_reg(r'(\d+[\u4e00-\u9fa5]{0,})', testText)
    print(road, search)

    for index, item in enumerate(search):
        address = {'road': road, 'level': index, 'content': item}
        print(address)
