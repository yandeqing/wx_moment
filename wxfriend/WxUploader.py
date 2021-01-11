#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/12/9 18:39
'''
import json
import os
import threading
from urllib import request

import requests

from common import FilePathUtil, excel_util, Logger
from wxfriend import wx_stop


def main_backgroud():
    thread = threading.Thread(target=main)
    thread.start()


def main(full_dir):
    Logger.println(f"【().full_dir={full_dir}】")
    array = excel_util.excel2array(full_dir)
    array = array[::-1]
    count = 0
    uploadItems(array)


def uploadItems(array):
    try:
        for index, item in enumerate(array):
            if wx_stop.stopFlag:
                break
            Logger.println(f"【({index}).item={item}】")
            res = requests.post("http://internal.zuker.im/moment", json=item)
            res_json = res.json()
            jsonstr = json.dumps(res_json, indent=4, ensure_ascii=False)
            Logger.println(f"【uploadItems({index}).res={jsonstr}】")
            if res_json['code'] == 20003:
                put_item(index, item)
                return '20003'
    except Exception as e:
        Logger.println(f"【e={e}】")
        pass


def uploadItem(item):
    try:
        Logger.println(f"uploadItem【item={item}】")
        res = requests.post("http://internal.zuker.im/moment", json=item)
        res_json = res.json()
        jsonstr = json.dumps(res_json, indent=4, ensure_ascii=False)
        Logger.println(f"【uploadItems().res={jsonstr}】")
        if res_json['code'] == 20003:
            return '20003'
    except Exception as e:
        Logger.println(f"【e={e}】")
        pass


def need_upload_photo_item(item):
    try:
        Logger.println(f"【item={item}】")
        res = requests.get("http://internal.zuker.im/moment", params=item)
        res_json = res.json()
        jsonstr = json.dumps(res_json, indent=4, ensure_ascii=False)
        Logger.println(f"【need_upload_photo_item().res={jsonstr}】")
        if res_json['code'] == 0:
            return not res_json['file_ids']
        else:
            return False
    except Exception as e:
        Logger.println(f"【e={e}】")
        return False


def putItems(array):
    try:
        for index, item in enumerate(array):
            if wx_stop.stopFlag:
                break
            put_item(index, item)
    except Exception as e:
        Logger.println(f"【e={e}】")
        pass


def put_item(index, item):
    Logger.println(f"【put_item({index}).item={item}】")
    res = requests.put("http://internal.zuker.im/moment", json=item)
    jsonstr = json.dumps(res.json(), indent=4, ensure_ascii=False)
    Logger.println(f"【({index}).res={jsonstr}】")


if __name__ == '__main__':
    full_dir = FilePathUtil.get_lastmodify_file(
        FilePathUtil.get_full_dir("wxfriend", "excel", "text"))
    main(full_dir)
