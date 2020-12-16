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

def main_backgroud():
    thread = threading.Thread(target=main)
    thread.start()

def main(full_dir):
    sheetname = os.path.basename(full_dir)[0:11]
    Logger.println(f"【().full_dir={full_dir}】")
    Logger.println(f"【().file={sheetname}】")
    array = excel_util.excel2array(full_dir, sheetname)
    array = array[::-1]
    count = 0
    for index, item in enumerate(array):
        Logger.println(f"【({index}).item={item}】")
        res = requests.post("http://internal.zuker.im/moment", json=item)
        jsonstr =json.dumps(res.json(),indent=4,ensure_ascii=False)
        Logger.println(f"【({index}).res={jsonstr}】")

if __name__ == '__main__':
    full_dir = FilePathUtil.get_lastmodify_file(
        FilePathUtil.get_full_dir("wxfriend", "excel", "text"))
    main(full_dir)