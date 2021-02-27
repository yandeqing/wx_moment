#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/2/7 13:19
'''
import re


def  search_text_by_reg(reg, text):
    try:
        search = re.search(reg, text)
        groups = search.group()
        return groups
    except:
        return None

def  find_texts_by_reg(reg, text):
    try:
        searchs = re.findall(reg, text)
        return searchs
    except:
        return None


if __name__ == '__main__':
    re.compile(r'asd$')

    search = find_texts_by_reg(r'[^\u4e00-\u9fa5a-zA-Z]', "测试你好111测试记你好211")
    print(f"【().search={search}】")
